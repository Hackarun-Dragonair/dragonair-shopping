"""Encaixa a voz gravada por uma pessoa no vídeo e calcula o tempo de cada fala.

Uso: python3 docs/pitch/video/alinhar_voz.py <tempos-guia.json> <voz-limpa.wav> <pasta_saida>
Saída: <pasta_saida>/voz-ajustada.wav (pronta para o vídeo) e <pasta_saida>/tempos-voz.json

Como decide:
  1. corta o silêncio do começo e do fim da gravação;
  2. se a fala passar do limite (vídeo de até 90 s), acelera no máximo 6% (atempo), sem cortar fala;
     se ainda assim passar, o vídeo fica um pouco mais longo (o regulamento aceita até 2 min);
     se a fala for curta, a cena final fica mais tempo na tela;
  3. acha as pausas da gravação e usa as maiores como troca de bloco do roteiro
     (problema, solução, IA, supervisor, acerto, diferencial, próximo passo); dentro de cada bloco,
     escolhe em ordem as pausas que melhor batem com a proporção da voz guia (troca de frase).
Só usa a biblioteca padrão do Python e o ffmpeg.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roteiro_video import FOLGA_FINAL, INICIO  # noqa: E402

guia = json.loads(Path(sys.argv[1]).read_text())
voz = Path(sys.argv[2])
saida = Path(sys.argv[3])
saida.mkdir(parents=True, exist_ok=True)

LIMITE_VIDEO = 90.0
MAX_ACELERA = 1.06


def duracao(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def silencios(arq, ruido="-38dB", minimo=0.25):
    """Lista de pausas (início, fim) achadas pelo silencedetect do ffmpeg."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(arq), "-af", f"silencedetect=noise={ruido}:d={minimo}",
                        "-f", "null", "-"], capture_output=True, text=True)
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    total = duracao(arq)
    fim += [total] * (len(ini) - len(fim))
    return list(zip(ini, fim)), total


# 1) onde a fala começa e termina
pausas, total = silencios(voz)
comeco = pausas[0][1] if pausas and pausas[0][0] < 0.05 else 0.0
final = pausas[-1][0] if pausas and pausas[-1][1] >= total - 0.05 else total
comeco = max(0.0, comeco - 0.05)
final = min(total, final + 0.15)
fala = final - comeco
if fala < 30:
    sys.exit(f"A gravação tem só {fala:.0f} s de fala. Confira se o arquivo é o certo (esperado: ~80 s).")

# 2) acelerar só se passar do limite
limite_fala = LIMITE_VIDEO - FOLGA_FINAL - INICIO
fator = min(MAX_ACELERA, fala / limite_fala) if fala > limite_fala else 1.0
fala_final = fala / fator
print(f"voz: {fala:.1f} s de fala; acelerada {100 * (fator - 1):.1f}% → {fala_final:.1f} s")

ajustada = saida / "voz-ajustada.wav"
filtros = [f"atrim={comeco:.3f}:{final:.3f}", "asetpts=PTS-STARTPTS"]
if fator > 1.0:
    filtros.append(f"atempo={fator:.4f}")
filtros += [f"adelay={int(INICIO * 1000)}:all=1", "loudnorm=I=-16:TP=-1.5:LRA=11", "aresample=48000"]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(voz), "-af", ",".join(filtros),
                "-ac", "1", "-ar", "48000", str(ajustada)], check=True)

# 3) alinhar blocos e falas
pausas, total = silencios(ajustada, minimo=0.3)
pausas = [(a, b) for a, b in pausas if a > INICIO + 0.3 and b < total - 0.1]
falas_g = guia["falas"]
g0, g1 = falas_g[0]["inicio"], falas_g[-1]["fim"]
h0, h1 = INICIO, INICIO + fala_final
escala = (h1 - h0) / (g1 - g0)


def proporcional(t):
    return h0 + (t - g0) * escala


blocos = []
for i, f in enumerate(falas_g):
    if i == 0 or f["bloco"] != falas_g[i - 1]["bloco"]:
        blocos.append(i)
inicio_bloco_h = {0: h0}
anterior = h0
for k in blocos[1:]:
    esperado = proporcional(falas_g[k]["inicio"])
    janela = max(3.0, 0.07 * (h1 - h0))
    candidatos = [(b - a) - 0.35 * abs(b - esperado) for a, b in pausas]
    melhor = None
    for (a, b), nota in zip(pausas, candidatos):
        if abs(b - esperado) <= janela and b > anterior + 2.0 and (melhor is None or nota > melhor[0]):
            melhor = (nota, b)
    inicio_bloco_h[k] = melhor[1] if melhor else esperado
    anterior = inicio_bloco_h[k]
    print(f"  bloco '{falas_g[k]['bloco']}': guia {falas_g[k]['inicio']:.1f} s → voz {inicio_bloco_h[k]:.1f} s"
          + ("" if melhor else " (sem pausa clara; usei a proporção)"))


limites = blocos + [len(falas_g)]
novas = []
for n, k in enumerate(blocos):
    ult = limites[n + 1] - 1
    gb = falas_g[ult]["fim"]
    ha = inicio_bloco_h[k]
    if n + 1 < len(blocos):
        # fim real do bloco na voz: começo da pausa que termina onde o próximo bloco começa
        prox = inicio_bloco_h[limites[n + 1]]
        antes = [a for a, b in pausas if abs(b - prox) < 0.01]
        hb = antes[0] if antes else prox - 0.3
    else:
        hb = h1
    # Dentro do bloco: cada troca de frase vai para uma pausa da gravação. Escolhe, em ordem,
    # o conjunto de pausas que fica mais perto da proporção da voz guia (programação dinâmica);
    # pausas mais longas valem mais. Se não houver pausa boa, usa a proporção.
    g0b = falas_g[k]["inicio"]
    previstos = [ha + (falas_g[i]["inicio"] - g0b) * (hb - ha) / max(gb - g0b, 0.1) for i in range(k + 1, ult + 1)]
    cand = [(a, b) for a, b in pausas if ha + 0.6 < b < hb]
    SEM = 1.4  # custo de não usar pausa nenhuma numa troca

    def custo(i, j):
        a, b = cand[j]
        return abs(b - previstos[i]) - 0.5 * min(b - a, 1.2)

    memo = {}

    def melhor(i, ultimo):
        """Menor custo para as trocas i.. sabendo que a última pausa usada foi 'ultimo'."""
        if i == len(previstos):
            return 0.0, []
        if (i, ultimo) in memo:
            return memo[(i, ultimo)]
        c, resto = melhor(i + 1, ultimo)
        opcao = (SEM + c, [None] + resto)
        for j in range(ultimo + 1, len(cand)):
            c, resto = melhor(i + 1, j)
            total_c = custo(i, j) + c
            if total_c < opcao[0]:
                opcao = (total_c, [j] + resto)
        memo[(i, ultimo)] = opcao
        return opcao

    escolha = melhor(0, -1)[1]
    comecos, fins_antes = [ha], []
    for i, j in enumerate(escolha):
        if j is None:
            comecos.append(previstos[i])
            fins_antes.append(previstos[i] - 0.2)
        else:
            fins_antes.append(cand[j][0])
            comecos.append(cand[j][1])
    fins_antes.append(hb)
    for j, i in enumerate(range(k, ult + 1)):
        f = falas_g[i]
        ini, fim = comecos[j], fins_antes[j]
        novas.append(dict(id=f["id"], texto=f["texto"], bloco=f["bloco"], inicio=round(ini, 3), fim=round(max(fim, ini + 0.6), 3)))
for a, b in zip(novas, novas[1:]):  # legenda nunca passa por cima da seguinte
    a["fim"] = min(a["fim"], b["inicio"] - 0.05)

(saida / "tempos-voz.json").write_text(json.dumps(dict(total=round(total, 3), fator=round(fator, 4), falas=novas),
                                                  ensure_ascii=False, indent=1))
print(f"tempos: {saida / 'tempos-voz.json'}")
