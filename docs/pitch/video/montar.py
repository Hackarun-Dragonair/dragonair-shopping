"""Monta o vídeo do pitch com ffmpeg: cenas, zoom suave, transições, legendas e áudio.

Uso:
  python3 docs/pitch/video/montar.py <pasta_trabalho> <tempos.json> <audio|silencio> <saida.mp4>

- <pasta_trabalho> tem telas/ (gravar_telas.py), cartelas/ (render_cartelas.py) e fontes/.
- <tempos.json> diz quando cada fala começa e termina (voz_guia.py ou alinhar_voz.py).
  As cenas se encaixam nesses tempos: se a voz muda, as imagens e as legendas acompanham.
- <audio>: arquivo de voz já tratado, ou a palavra "silencio" (trilha muda).
Só usa a biblioteca padrão do Python e o ffmpeg.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roteiro_video import DURACAO  # noqa: E402

TRAB = Path(sys.argv[1]).resolve()
TEMPOS = json.loads(Path(sys.argv[2]).read_text())
AUDIO = sys.argv[3]
SAIDA = Path(sys.argv[4]).resolve()
CENAS = TRAB / "cenas"
CENAS.mkdir(exist_ok=True)
MARCAS = json.loads((TRAB / "telas" / "marcas.json").read_text())
CEL, PC = MARCAS["celular"], MARCAS["computador"]
FPS = 30
XF = 0.4  # duração da transição entre cenas (fade)

F = [f["inicio"] for f in TEMPOS["falas"]]  # início de cada fala
FIM_FALA = TEMPOS["falas"][-1]["fim"]
TOTAL = round(max(DURACAO, FIM_FALA + 3.0), 2)


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-hide_banner", *map(str, args)], check=True)


# ---------- geometria ----------
# Celular: a tela do app (780x1688) vai para o buraco da moldura, na composição 3840x2160.
TELA_X, TELA_Y, TELA_L, TELA_A = 680, 130, 880, 1900


def cel_xy(x, y):
    return TELA_X + x * TELA_L / 780, TELA_Y + y * TELA_A / 1688


def centro_cel(caixa):
    x, y, w, h = caixa
    return cel_xy(x + w / 2, y + h / 2)


def centro_pc(caixa):
    x, y, w, h = caixa
    return x + w / 2, y + h / 2


# ---------- zoom (ken burns) com zoompan ----------
def interp(chaves, i, t="t"):
    """Expressão ffmpeg que vai suavemente (smoothstep) de uma chave para a seguinte."""
    expr = f"{chaves[-1][i]:.4f}"
    for k in range(len(chaves) - 2, -1, -1):
        t0, t1 = chaves[k][0], chaves[k + 1][0]
        v0, v1 = chaves[k][i], chaves[k + 1][i]
        if t1 - t0 < 1e-3:
            continue
        u = f"(({t}-{t0:.3f})/{t1 - t0:.3f})"
        expr = f"if(lt({t},{t1:.3f}),{v0:.4f}+({v1 - v0:.4f})*{u}*{u}*(3-2*{u}),{expr})"
    return f"if(lt({t},{chaves[0][0]:.3f}),{chaves[0][i]:.4f},{expr})"


def zoompan(chaves, larg, alt, saida="1920x1080"):
    """chaves = [(t, zoom, cx, cy)] em segundos da saída e pixels da entrada (larg x alt)."""
    if not chaves:
        chaves = [(0, 1.0, larg / 2, alt / 2)]
    t = f"(on/{FPS})"
    z = interp(chaves, 1, t)
    cx, cy = interp(chaves, 2, t), interp(chaves, 3, t)
    x = f"max(0,min(iw-iw/zoom,({cx})-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,({cy})-ih/zoom/2))"
    return f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={saida}:fps={FPS}"


def zoom_em(centro, z, dur, entra=0.7, sai=None, inicio=0.0, de=(1.0, None)):
    """Atalho: parte de z=1 (ou do zoom 'de'), chega em z no centro dado e fica (ou sai no fim)."""
    cx, cy = centro
    z0, c0 = de
    c0 = c0 or centro
    chaves = [(inicio, z0, *c0), (inicio + entra, z, cx, cy)]
    if sai:
        chaves += [(dur - sai, z, cx, cy), (dur, z0, *c0)]
    return chaves


# ---------- trechos de gravação ----------
def trecho(fonte, a, b, vel=1.0, zoom=None, fundo=None):
    return dict(fonte=fonte, a=a, b=b, vel=vel, zoom=zoom or [], fundo=fundo)


def render_trechos(nome, trechos, dur, elastico=-1):
    """Cada trecho vira um mp4 1920x1080; a cena junta todos e completa o tempo congelando um trecho."""
    natural = sum((t["b"] - t["a"]) / t["vel"] for t in trechos)
    acelera = max(1.0, natural / dur)
    sobra = max(0.0, dur - natural / acelera)
    partes = []
    for i, t in enumerate(trechos):
        vel = t["vel"] * acelera
        dur_saida = (t["b"] - t["a"]) / vel
        extra = sobra if i == (elastico % len(trechos)) else 0.0
        arq = CENAS / f"{nome}_{i}.mp4"
        congela = f",tpad=stop_mode=clone:stop_duration={extra:.3f}" if extra > 0 else ""
        base = f"setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS}{congela}"
        corte = ["-ss", f"{t['a']:.3f}", "-t", f"{t['b'] - t['a']:.3f}"]
        total = dur_saida + extra
        zoom = [(max(0.0, k[0]), *k[1:]) for k in t["zoom"]]
        if t["fonte"] == "pc":
            filtro = f"[0:v]{base},{zoompan(zoom, 3072, 1728)},format=yuv420p[v]"
            entradas = [*corte, "-i", TRAB / "telas" / "computador.mp4"]
        else:
            # O zoom mexe só na metade esquerda (celular); a coluna da direita (passos e legenda) fica parada.
            filtro = (f"[0:v]split[f1][f2];[1:v]{base},scale={TELA_L}:{TELA_A}:flags=lanczos[tela];"
                      f"[f1][tela]overlay={TELA_X}:{TELA_Y}:shortest=1[c];[c][2:v]overlay=0:0,crop=1880:2160:0:0,"
                      f"{zoompan(zoom, 1880, 2160, '940x1080')}[esq];"
                      f"[f2]crop=1960:2160:1880:0,scale=980:1080:flags=lanczos[dir];"
                      f"[esq][dir]hstack=2,format=yuv420p[v]")
            entradas = ["-loop", "1", "-framerate", FPS, "-i", TRAB / "cartelas" / f"{t['fundo']}.png",
                        *corte, "-i", TRAB / "telas" / "celular.mp4",
                        "-loop", "1", "-framerate", FPS, "-i", TRAB / "cartelas" / "moldura.png"]
        ffmpeg(*entradas, "-filter_complex", filtro, "-map", "[v]", "-t", f"{total:.3f}",
               "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, arq)
        partes.append(arq)
    lista = CENAS / f"{nome}.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in partes))
    saida = CENAS / f"{nome}.mp4"
    ffmpeg("-f", "concat", "-safe", "0", "-i", lista, "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "fast",
           "-crf", "12", "-r", FPS, "-pix_fmt", "yuv420p", saida)
    return saida


def render_cartela(nome, imagens, dur, z_fim=1.06, centro=None):
    """Cartela parada com zoom lento. imagens = [(png, segundo_em_que_entra)], com fusão entre elas."""
    saida = CENAS / f"{nome}.mp4"
    cx, cy = centro or (1920, 1080)
    zp = zoompan([(0, 1.0, 1920, 1080), (dur, z_fim, cx, cy)], 3840, 2160)
    entradas, filtros = [], []
    for i, (png, _) in enumerate(imagens):
        entradas += ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}", "-i", TRAB / "cartelas" / f"{png}.png"]
    atual = "[0:v]"
    for i, (_, quando) in enumerate(imagens[1:], start=1):
        filtros.append(f"{atual}[{i}:v]xfade=transition=fade:duration=0.5:offset={quando:.3f}[x{i}]")
        atual = f"[x{i}]"
    filtros.append(f"{atual}format=yuv420p,{zp},format=yuv420p[v]")
    ffmpeg(*entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, saida)
    return saida


# ---------- roteiro de cenas (início de cada uma, preso às falas) ----------
inicios = {
    "abertura": 0.0,
    "hoje": F[2] - 0.35,
    "solucao": F[4] - 0.35,
    "cel_qr": F[6] - 0.25,
    "cel_problema": F[9] - 0.3,
    "gestor": F[14] - 0.35,
    "mapa": F[17] - 0.2,
    "painel": F[18] - 0.2,
    "ia": F[19] - 0.45,
    "diferencial": F[21] - 0.35,
    "mapa_cinza": F[22] - 0.2,
    "fim": F[23] - 0.35,
}
ordem = list(inicios)
duracoes = {}
for i, nome in enumerate(ordem):
    prox = inicios[ordem[i + 1]] if i + 1 < len(ordem) else TOTAL
    duracoes[nome] = prox - inicios[nome] + (XF if i + 1 < len(ordem) else 0.0)


def cena(nome):
    d = duracoes[nome]
    print(f"cena {nome:13s} {inicios[nome]:6.2f}s  dura {d:5.2f}s")
    if nome == "abertura":
        return render_cartela(nome, [("abertura", 0)], d, 1.07, (1500, 1000))
    if nome == "hoje":
        troca = F[3] - inicios["hoje"] - 0.2  # o rádio acende quando a fala chega nele
        return render_cartela(nome, [("hoje-a", 0), ("hoje", troca)], d, 1.05, (1920, 1150))
    if nome == "solucao":
        return render_cartela(nome, [("solucao", 0)], d, 1.06)
    if nome == "diferencial":
        return render_cartela(nome, [("diferencial", 0)], d, 1.05, (2500, 1150))
    if nome == "fim":
        return render_cartela(nome, [("fim", 0)], d, 1.04)
    c = CEL
    if nome == "cel_qr":
        return render_trechos(nome, [
            trecho("cel", c["zona"]["t"] - 0.5, c["zona"]["t"] + 2.0, fundo="fundo-cel-qr"),
            trecho("cel", c["toque_problema"]["t"] - 0.5, c["toque_problema"]["t"] + 0.5, fundo="fundo-cel-qr"),
        ], d, elastico=0)
    if nome == "cel_problema":
        sug, ele = c["sugestao"], c["toque_eletrica"]
        z_duvida = centro_cel(sug["desempate"])
        z_alerta = centro_cel(c["registrado"]["resultado"])
        return render_trechos(nome, [
            trecho("cel", c["toque_problema"]["t"] + 0.5, c["comeca_digitar"]["t"], 1.4, fundo="fundo-cel-passo1"),
            trecho("cel", c["comeca_digitar"]["t"], c["digitou"]["t"] + 0.3, 1.0, fundo="fundo-cel-passo1",
                   zoom=zoom_em(centro_cel([58, 500, 664, 300]), 1.3, 3.0, entra=0.8)),
            trecho("cel", c["digitou"]["t"] + 0.3, c["toque_sugestao"]["t"] + 0.5, 1.3, fundo="fundo-cel-passo2"),
            trecho("cel", c["toque_sugestao"]["t"] + 0.5, sug["t"] + 0.1, 1.3, fundo="fundo-cel-passo2"),
            trecho("cel", sug["t"] + 0.1, ele["t"] + 1.0, 1.0, fundo="fundo-cel-passo3",
                   zoom=zoom_em(z_duvida, 1.45, 0, entra=0.8)),
            trecho("cel", ele["t"] + 1.0, c["toque_registrar"]["t"] + 0.2, 1.0, fundo="fundo-cel-passo4",
                   zoom=zoom_em(z_duvida, 1.45, 0, entra=0.6, de=(1.45, z_duvida))),
            trecho("cel", c["toque_registrar"]["t"] + 0.2, c["registrado"]["t"] + 2.5, 1.0, fundo="fundo-cel-passo4",
                   zoom=zoom_em(z_alerta, 1.45, 0, entra=0.9)),
        ], d)
    p = PC
    if nome == "gestor":
        cartao = centro_pc(p["fila"]["cartao"])
        prio = centro_pc(p["escolheu_p3"]["prioridade"])
        aviso = centro_pc(p["mantida"]["aviso"])
        linha = centro_pc(p["mantida"]["linha"])
        return render_trechos(nome, [
            trecho("pc", p["fila"]["t"] + 1.9, p["problema"]["t"] - 1.2, 1.2,
                   zoom=zoom_em((cartao[0] + 300, cartao[1] - 100), 1.35, 0, entra=0.01)),
            trecho("pc", p["escolheu_p3"]["t"] - 0.6, p["clicou_confirmar"]["t"] + 0.3, 1.4,
                   zoom=zoom_em((prio[0] + 500, prio[1] + 60), 1.55, 0, entra=0.01)),
            trecho("pc", p["mantida"]["t"] - 0.05, p["mantida"]["t"] + 2.3, 1.0,
                   zoom=zoom_em((aviso[0] + 250, aviso[1] - 150), 1.5, 0, entra=0.01, de=(1.15, (1536, 864)))),
            trecho("pc", p["linha_tempo"]["t"] - 1.8, p["linha_tempo"]["t"] + 1.2, 1.2,
                   zoom=zoom_em(linha, 1.45, 0, entra=0.8)),
        ], d, elastico=2)
    if nome == "mapa":
        svg = centro_pc(p["mapa_caixas"]["svg"])
        return render_trechos(nome, [
            trecho("pc", p["mapa"]["t"] + 0.2, p["mapa"]["t"] + 4.6, 1.0,
                   zoom=[(0, 1.0, 1536, 864), (d, 1.18, svg[0] + 150, svg[1])]),
        ], d)
    if nome == "painel":
        return render_trechos(nome, [
            trecho("pc", p["painel"]["t"] + 0.1, p["painel_fim"]["t"] + 1.0, 1.0,
                   zoom=[(0, 1.0, 1536, 864), (d, 1.22, 1250, 760)]),
        ], d)
    if nome == "ia":
        num = centro_pc(p["ia"]["numeros"])
        tab = centro_pc(p["ia_tabela"]["tabela"])
        t_tab = F[20] - inicios["ia"] - 0.3  # vai para a tabela quando a fala diz "o teste é pequeno"
        return render_trechos(nome, [
            trecho("pc", p["ia"]["t"] + 0.1, p["ia_tabela"]["t"] + 3.4, 1.0,
                   zoom=[(0, 1.0, 1536, 864), (1.0, 1.55, num[0], num[1] - 60),
                         (t_tab, 1.55, num[0], num[1] - 60), (t_tab + 1.0, 1.5, tab[0], tab[1])]),
        ], d)
    if nome == "mapa_cinza":
        cinzas = [centro_pc(cx) for cx in p["mapa_caixas"]["cinzas"]]
        mx = sum(c[0] for c in cinzas) / len(cinzas)
        my = sum(c[1] for c in cinzas) / len(cinzas)
        return render_trechos(nome, [
            trecho("pc", p["mapa_caixas"]["t"] + 0.5, p["mapa_fim"]["t"], 1.4,
                   zoom=[(0, 1.3, mx, my), (d, 1.5, mx, my)]),
        ], d)
    raise ValueError(nome)


# ---------- legendas (ASS) ----------
def tempo_ass(s):
    s = max(0.0, s)
    h, m = int(s // 3600), int(s % 3600 // 60)
    return f"{h}:{m:02d}:{s % 60:05.2f}"


def quebrar(texto, largura):
    """Quebra em linhas equilibradas de até 'largura' caracteres."""
    palavras, linhas, atual = texto.split(), [], ""
    n_linhas = max(1, -(-len(texto) // largura))
    alvo = len(texto) / n_linhas
    for p in palavras:
        if atual and len(atual) + 1 + len(p) > max(alvo + 6, 1) and len(linhas) < n_linhas - 1:
            linhas.append(atual)
            atual = p
        else:
            atual = f"{atual} {p}".strip()
    linhas.append(atual)
    return r"\N".join(linhas)


SECOES = [
    ("abertura", "1 · O PROBLEMA"),
    ("solucao", "2 · A SOLUÇÃO"),
    ("cel_problema", "3 · FUNCIONALIDADES · IA + REGRA DE RISCO"),
    ("gestor", "3 · FUNCIONALIDADES · GESTOR E LINHA DO TEMPO"),
    ("mapa", "3 · FUNCIONALIDADES · MAPA AO VIVO"),
    ("painel", "3 · FUNCIONALIDADES · PAINEL"),
    ("ia", "3 · FUNCIONALIDADES · ACERTO REAL DA IA"),
    ("diferencial", "4 · DIFERENCIAL"),
    ("fim", None),
]
CENAS_CEL = ("cel_qr", "cel_problema")
CENAS_PC = ("gestor", "mapa", "painel", "ia")


def cena_em(t):
    atual = ordem[0]
    for nome in ordem:
        if inicios[nome] <= t + 1e-6:
            atual = nome
    return atual


def legendas():
    cab = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Baixo,Montserrat SemiBold,52,&H00FFFFFF,&H00FFFFFF,&H281B242C,&H00000000,0,0,0,0,100,100,0,0,3,16,0,2,150,150,44,1
Style: Lateral,Montserrat SemiBold,48,&H00FFFFFF,&H00FFFFFF,&H281B242C,&H00000000,0,0,0,0,100,100,0,0,3,16,0,2,1080,70,70,1
Style: Secao,Montserrat,30,&H00EFF4F6,&H00EFF4F6,&H00325C7A,&H00000000,-1,0,0,0,100,100,2,0,3,11,0,8,150,150,20,1
Style: SecaoPC,Montserrat,30,&H00EFF4F6,&H00EFF4F6,&H00325C7A,&H00000000,-1,0,0,0,100,100,2,0,3,11,0,9,40,28,20,1
Style: SecaoLateral,Montserrat,30,&H00EFF4F6,&H00EFF4F6,&H00325C7A,&H00000000,-1,0,0,0,100,100,2,0,3,11,0,8,1080,70,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    linhas = []
    falas = TEMPOS["falas"]
    for i, f in enumerate(falas):
        ini = f["inicio"] - 0.12
        fim = f["fim"] + 0.35
        if i + 1 < len(falas):
            fim = min(fim, falas[i + 1]["inicio"] - 0.15)
        else:
            fim = TOTAL - 0.6
        lateral = cena_em(f["inicio"]) in CENAS_CEL
        estilo = "Lateral" if lateral else "Baixo"
        texto = quebrar(f["texto"], 26 if lateral else 52)
        linhas.append(f"Dialogue: 1,{tempo_ass(ini)},{tempo_ass(fim)},{estilo},,0,0,0,,{{\\fad(120,120)}}{texto}")
    for k, (nome, rotulo) in enumerate(SECOES):
        if not rotulo:
            continue
        ini = inicios[nome] + (0.25 if k else 0.3)
        fim = inicios[SECOES[k + 1][0]] - 0.05
        # nas cenas de celular o rótulo vai para a coluna da direita
        partes = [(ini, fim)]
        for cel in CENAS_CEL:
            ci = inicios[cel]
            cf = inicios[ordem[ordem.index(cel) + 1]]
            novas = []
            for a, b in partes:
                if b <= ci or a >= cf:
                    novas.append((a, b))
                    continue
                if a < ci:
                    novas.append((a, ci))
                linhas.append(f"Dialogue: 0,{tempo_ass(max(a, ci))},{tempo_ass(min(b, cf))},SecaoLateral,,0,0,0,,{{\\fad(150,0)}}{rotulo}")
                if b > cf:
                    novas.append((cf, b))
            partes = novas
        estilo = "SecaoPC" if nome in CENAS_PC else "Secao"
        for a, b in partes:
            linhas.append(f"Dialogue: 0,{tempo_ass(a)},{tempo_ass(b)},{estilo},,0,0,0,,{{\\fad(150,150)}}{rotulo}")
    arq = CENAS / "legendas.ass"
    arq.write_text(cab + "\n".join(linhas) + "\n", encoding="utf-8")
    return arq


# ---------- montagem ----------
def montar():
    # Se as imagens não mudaram (mesmos tempos, gravação, cartelas e script), reaproveita a base pronta.
    base = CENAS / "base.mp4"
    marca = hashlib.sha256()
    for arq in [Path(__file__), TRAB / "telas" / "marcas.json", *sorted((TRAB / "cartelas").glob("*.png"))]:
        marca.update(arq.read_bytes())
    marca.update(json.dumps([inicios, TOTAL]).encode())
    assinatura = CENAS / "base.assinatura"
    if base.exists() and assinatura.exists() and assinatura.read_text() == marca.hexdigest():
        print("imagens iguais às da última montagem: reaproveitando a base")
        return finalizar(base)
    arquivos = [cena(n) for n in ordem]
    entradas, filtros = [], []
    for a in arquivos:
        entradas += ["-i", a]
    atual, acumulado = "[0:v]", 0.0
    for i in range(1, len(arquivos)):
        acumulado = inicios[ordem[i]]
        filtros.append(f"{atual}[{i}:v]xfade=transition=fade:duration={XF}:offset={acumulado:.3f}[x{i}]")
        atual = f"[x{i}]"
    filtros.append(f"{atual}format=yuv420p[v]")
    ffmpeg(*entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-t", f"{TOTAL:.3f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "12", "-r", FPS, base)
    assinatura.write_text(marca.hexdigest())
    finalizar(base)


def finalizar(base):
    ass = legendas()
    fontes = TRAB / "fontes"
    vf = f"ass={ass}:fontsdir={fontes},format=yuv420p"
    if AUDIO == "silencio":
        audio = ["-f", "lavfi", "-t", f"{TOTAL:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        af = []
    else:
        audio = ["-i", AUDIO]
        af = ["-af", f"apad,atrim=0:{TOTAL:.3f},aresample=48000"]
    ffmpeg("-i", base, *audio, "-map", "0:v", "-map", "1:a", "-vf", vf, *af,
           "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-maxrate", "4500k", "-bufsize", "9000k",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", FPS,
           "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-ar", "48000",
           "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", SAIDA)
    print(f"pronto: {SAIDA} ({TOTAL:.1f} s)")


if __name__ == "__main__":
    montar()
