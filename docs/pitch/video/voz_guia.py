"""Gera a voz guia sintética (Piper, offline) e o tempo de cada fala.

Uso: <venv-do-piper>/bin/python docs/pitch/video/voz_guia.py <modelo.onnx> <pasta_saida> [velocidade]
Saída: <pasta_saida>/voz-guia.wav (mono 22 kHz, sem tratamento) e <pasta_saida>/tempos.json
O tempos.json é a base das legendas e da montagem: cada fala ganha início e fim em segundos.
"""
import json
import sys
import wave
from pathlib import Path

from piper import PiperVoice, SynthesisConfig

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roteiro_video import ANCORAS, FALAS, INICIO  # noqa: E402

modelo, saida = sys.argv[1], Path(sys.argv[2])
velocidade = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0  # length_scale: >1 fala mais devagar
saida.mkdir(parents=True, exist_ok=True)
voz = PiperVoice.load(modelo)
config = SynthesisConfig(length_scale=velocidade, noise_scale=0.6, noise_w_scale=0.8)
taxa = voz.config.sample_rate


def sintetizar(texto: str) -> bytes:
    """Áudio PCM 16 bits da fala, sem o silêncio que sobra nas pontas."""
    pcm = b"".join(parte.audio_int16_bytes for parte in voz.synthesize(texto, syn_config=config))
    amostras = memoryview(pcm).cast("h")
    limiar = 300
    ini = next((i for i, a in enumerate(amostras) if abs(a) > limiar), 0)
    fim = len(amostras) - next((i for i, a in enumerate(reversed(amostras)) if abs(a) > limiar), 0)
    ini = max(0, ini - int(0.02 * taxa))
    fim = min(len(amostras), fim + int(0.06 * taxa))
    return bytes(amostras[ini:fim].cast("B"))


tempos, audio = [], bytearray(b"\x00\x00" * int(INICIO * taxa))
bloco_atual = None
for fala in FALAS:
    if fala["bloco"] != bloco_atual:  # bloco novo: espera até a âncora do roteiro
        bloco_atual = fala["bloco"]
        falta = ANCORAS[bloco_atual] - len(audio) / 2 / taxa
        audio += b"\x00\x00" * max(0, int(falta * taxa))
    pcm = sintetizar(fala["tts"])
    ini = len(audio) / 2 / taxa
    audio += pcm
    fim = len(audio) / 2 / taxa
    audio += b"\x00\x00" * int(fala["pausa"] * taxa)
    tempos.append(dict(texto=fala["texto"], bloco=fala["bloco"], inicio=round(ini, 3), fim=round(fim, 3)))

with wave.open(str(saida / "voz-guia.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(taxa)
    w.writeframes(bytes(audio))

total = len(audio) / 2 / taxa
(saida / "tempos.json").write_text(json.dumps(dict(total=round(total, 3), falas=tempos), ensure_ascii=False, indent=1))
print(f"voz guia: {total:.1f} s, {len(tempos)} falas")
for t in tempos:
    print(f"  {t['inicio']:6.2f}–{t['fim']:6.2f}  {t['bloco']:11s} {t['texto']}")
