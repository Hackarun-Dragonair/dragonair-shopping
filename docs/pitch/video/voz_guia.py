"""Gera a voz guia sintética (Piper, offline) e o tempo de cada fala.

Uso: <venv-do-piper>/bin/python docs/pitch/video/voz_guia.py <modelo.onnx> <pasta_saida> [velocidade_base]
Saída: <pasta_saida>/voz-guia.wav (mono 22 kHz, sem tratamento) e <pasta_saida>/tempos.json
O tempos.json é a base das legendas e da montagem: cada fala ganha início e fim em segundos.

Ritmo: cada frase fica com no máximo MAX_PALAVRAS_SEG palavras por segundo (contando a pausa
que vem depois) e no máximo 2,9 palavras por segundo só na fala. Se a voz sair rápida demais,
a frase é sintetizada de novo mais devagar.
"""
import json
import sys
import wave
from pathlib import Path

from piper import PiperVoice, SynthesisConfig

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roteiro_video import FALAS, INICIO, MAX_PALAVRAS_SEG, PAUSA_BLOCO, palavras  # noqa: E402

modelo, saida = sys.argv[1], Path(sys.argv[2])
base = float(sys.argv[3]) if len(sys.argv) > 3 else 1.05  # length_scale: >1 fala mais devagar
saida.mkdir(parents=True, exist_ok=True)
voz = PiperVoice.load(modelo)
taxa = voz.config.sample_rate


def sintetizar(texto: str, escala: float) -> bytes:
    """Áudio PCM 16 bits da fala, sem o silêncio que sobra nas pontas."""
    config = SynthesisConfig(length_scale=escala, noise_scale=0.6, noise_w_scale=0.8)
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
    if bloco_atual is not None and fala["bloco"] != bloco_atual:
        audio += b"\x00\x00" * int(PAUSA_BLOCO * taxa)
    bloco_atual = fala["bloco"]
    n = palavras(fala["texto"])
    alvo = max(n / MAX_PALAVRAS_SEG - fala["pausa"], n / 2.9)
    escala = base
    for _ in range(3):  # fala mais devagar até caber no ritmo
        pcm = sintetizar(fala["tts"], escala)
        dur = len(pcm) / 2 / taxa
        if dur >= alvo - 0.05 or escala >= 1.7:
            break
        escala = min(1.7, escala * alvo / dur * 1.02)
    ini = len(audio) / 2 / taxa
    audio += pcm
    fim = len(audio) / 2 / taxa
    pausa = max(fala["pausa"], n / MAX_PALAVRAS_SEG - (fim - ini))
    audio += b"\x00\x00" * int(pausa * taxa)
    tempos.append(dict(id=fala["id"], texto=fala["texto"], bloco=fala["bloco"], inicio=round(ini, 3), fim=round(fim, 3)))

with wave.open(str(saida / "voz-guia.wav"), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(taxa)
    w.writeframes(bytes(audio))

total = len(audio) / 2 / taxa
(saida / "tempos.json").write_text(json.dumps(dict(total=round(total, 3), falas=tempos), ensure_ascii=False, indent=1))
print(f"voz guia: {total:.1f} s, {len(tempos)} falas, {palavras()} palavras")
for i, t in enumerate(tempos):
    prox = tempos[i + 1]["inicio"] if i + 1 < len(tempos) else total
    ritmo = palavras(t["texto"]) / (prox - t["inicio"])
    print(f"  {t['inicio']:6.2f}–{t['fim']:6.2f}  {ritmo:4.2f} p/s  {t['id']:3s} {t['texto']}")
