"""Monta o vídeo do pitch com ffmpeg: cenas, zoom suave, transições, legendas e áudio.

Uso:
  python3 docs/pitch/video/montar.py <pasta_trabalho> <tempos.json> <audio|silencio> <saida.mp4>

- <pasta_trabalho> tem telas/ (gravar_telas.py), cartelas/ (render_cartelas.py) e fontes/.
- <tempos.json> diz quando cada fala começa e termina (voz_guia.py ou alinhar_voz.py).
  Cada cena e cada trecho de tela ficam presos a uma fala (pelo id): se a voz muda,
  as imagens e as legendas acompanham.
- <audio>: arquivo de voz já tratado, ou a palavra "silencio" (trilha muda).
Só usa a biblioteca padrão do Python e o ffmpeg.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roteiro_video import DURACAO_MIN, FOLGA_FINAL  # noqa: E402

TRAB = Path(sys.argv[1]).resolve()
TEMPOS = json.loads(Path(sys.argv[2]).read_text())
AUDIO = sys.argv[3]
SAIDA = Path(sys.argv[4]).resolve()
CENAS = TRAB / "cenas"
CENAS.mkdir(exist_ok=True)
MARCAS = json.loads((TRAB / "telas" / "marcas.json").read_text())
AB, CEL, PC = MARCAS["abertura"], MARCAS["celular"], MARCAS["computador"]
FPS = 30
XF = 0.35  # duração da transição entre cenas (fade)
CORTE_SECO = {"ia"}  # cenas que entram com corte seco (a fusão mostraria o topo da tela da IA)

T = {f["id"]: f["inicio"] for f in TEMPOS["falas"]}  # início de cada fala
E = {f["id"]: f["fim"] for f in TEMPOS["falas"]}     # fim de cada fala
FIM_FALA = TEMPOS["falas"][-1]["fim"]
TOTAL = round(max(DURACAO_MIN, FIM_FALA + FOLGA_FINAL), 2)


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-hide_banner", *map(str, args)], check=True)


def m(fonte, nome):
    return fonte[nome]["t"]


# ---------- geometria ----------
# Celular: a tela do app (780x1688) vai para o buraco da moldura, na composição 3840x2160.
TELA_X, TELA_Y, TELA_L, TELA_A = 680, 130, 880, 1900


def cel_xy(x, y):
    return TELA_X + x * TELA_L / 780, TELA_Y + y * TELA_A / 1688


def centro_cel(*caixas):
    """Centro do retângulo que cobre todas as caixas (pixels da tela do celular → composição)."""
    x0 = min(c[0] for c in caixas)
    y0 = min(c[1] for c in caixas)
    x1 = max(c[0] + c[2] for c in caixas)
    y1 = max(c[1] + c[3] for c in caixas)
    return cel_xy((x0 + x1) / 2, (y0 + y1) / 2)


def centro_pc(caixa, dx=0, dy=0):
    x, y, w, h = caixa
    return x + w / 2 + dx, y + h / 2 + dy


# ---------- zoom (ken burns) com zoompan ----------
def interp(chaves, i, t):
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


def fixo(z, centro, de=None, entra=0.7):
    """Zoom que vai de 'de' (zoom, centro) para (z, centro) em 'entra' segundos e fica."""
    cx, cy = centro
    if de is None:
        return [(0, z, cx, cy)]
    return [(0, de[0], *de[1]), (entra, z, cx, cy)]


# ---------- trechos de gravação ----------
def trecho(fonte, a, b, vel=1.0, zoom=None, fundo=None, em=None):
    """Pedaço da gravação [a, b] (segundos). 'em' = segundo do vídeo em que ele deve começar."""
    return dict(fonte=fonte, a=a, b=b, vel=vel, zoom=zoom or [], fundo=fundo, em=em)


ARQ = {"pc": "computador.mp4", "cel": "celular.mp4", "abertura": "abertura.mp4"}


def render_um(arq, t, vel, extra):
    """Um trecho vira um mp4 1920x1080 (com o último quadro congelado por 'extra' segundos)."""
    dur_saida = (t["b"] - t["a"]) / vel
    congela = f",tpad=stop_mode=clone:stop_duration={extra:.3f}" if extra > 0 else ""
    base = f"setpts=(PTS-STARTPTS)/{vel:.4f},fps={FPS}{congela}"
    corte = ["-ss", f"{t['a']:.3f}", "-t", f"{t['b'] - t['a']:.3f}"]
    zoom = [(k[0] / (vel / t["vel"]), *k[1:]) for k in t["zoom"]]  # se acelerou, o zoom acompanha
    if t["fonte"] in ("pc", "abertura"):
        filtro = f"[0:v]{base},{zoompan(zoom, 3072, 1728)},format=yuv420p[v]"
        entradas = [*corte, "-i", TRAB / "telas" / ARQ[t["fonte"]]]
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
    ffmpeg(*entradas, "-filter_complex", filtro, "-map", "[v]", "-t", f"{dur_saida + extra:.3f}",
           "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, arq)


def render_trechos(nome, trechos, inicio, dur):
    """Junta os trechos. Os que têm 'em' começam no segundo certo; entre duas âncoras,
    acelera se faltar tempo ou congela o último quadro do grupo se sobrar."""
    grupos, atual = [], []
    for t in trechos:
        if t["em"] is not None and atual:
            grupos.append(atual)
            atual = []
        atual.append(t)
    grupos.append(atual)
    partes, i = [], 0
    for k, g in enumerate(grupos):
        g_ini = inicio if k == 0 else g[0]["em"]
        g_fim = grupos[k + 1][0]["em"] if k + 1 < len(grupos) else inicio + dur
        espaco = max(0.3, g_fim - g_ini)
        natural = sum((t["b"] - t["a"]) / t["vel"] for t in g)
        acelera = max(1.0, natural / espaco)
        sobra = max(0.0, espaco - natural / acelera)
        for j, t in enumerate(g):
            arq = CENAS / f"{nome}_{i}.mp4"
            render_um(arq, t, t["vel"] * acelera, sobra if j == len(g) - 1 else 0.0)
            partes.append(arq)
            i += 1
    lista = CENAS / f"{nome}.txt"
    lista.write_text("".join(f"file '{p}'\n" for p in partes))
    saida = CENAS / f"{nome}.mp4"
    ffmpeg("-f", "concat", "-safe", "0", "-i", lista, "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "fast",
           "-crf", "12", "-r", FPS, "-pix_fmt", "yuv420p", saida)
    return saida


def render_cartela(nome, imagens, dur, z_fim=1.06, centro=None):
    """Cartela com zoom lento. imagens = [(png, segundo_em_que_entra)], com fusão entre elas."""
    saida = CENAS / f"{nome}.mp4"
    cx, cy = centro or (1920, 1080)
    zp = zoompan([(0, 1.0, 1920, 1080), (dur, z_fim, cx, cy)], 3840, 2160)
    entradas, filtros = [], []
    for png, _ in imagens:
        entradas += ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}", "-i", TRAB / "cartelas" / f"{png}.png"]
    atual = "[0:v]"
    for i, (_, quando) in enumerate(imagens[1:], start=1):
        filtros.append(f"{atual}[{i}:v]xfade=transition=fade:duration=0.5:offset={quando:.3f}[x{i}]")
        atual = f"[x{i}]"
    filtros.append(f"{atual}format=yuv420p,{zp},format=yuv420p[v]")
    ffmpeg(*entradas, "-filter_complex", ";".join(filtros), "-map", "[v]", "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, saida)
    return saida


def render_gancho(nome, dur):
    """Abertura: o mapa real com zonas cinza se aproximando devagar e, por cima, a pergunta entrando."""
    # Enquadra só o desenho do mapa: a borda direita do quadro nunca passa do fim do mapa,
    # então a coluna de indicadores (com "100% Acerto da IA") fica de fora.
    x, y, w, h = AB["mapa"]["svg"]
    direita, cy = x + w + 20, y + h / 2

    def centro_x(z):
        return direita - 3072 / z / 2

    fundo = CENAS / f"{nome}_mapa.mp4"
    render_um(fundo, trecho("abertura", m(AB, "mapa") + 0.2, m(AB, "mapa") + 0.2 + dur,
                            zoom=[(0, 1.45, centro_x(1.45), cy), (dur, 1.7, centro_x(1.7), cy + 60)]), 1.0, 0.0)
    t_rot = 0.25
    t_l1 = T["p2"] - 0.15
    t_l2 = T["p2"] + 0.85

    def camada(png):
        return ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}", "-i", TRAB / "cartelas" / f"{png}.png"]

    def entra(i, t0, dx):
        """Camada i aparece em t0: some → aparece (0,5 s) deslizando dx pixels."""
        return (f"[{i}:v]scale=1920:1080,format=rgba,fade=t=in:st={t0:.2f}:d=0.5:alpha=1[c{i}]",
                f"x='-{dx}*pow(1-min(1,max(0,(t-{t0:.2f})/0.5)),2)'")
    filtros, xs = [], {}
    for i, (t0, dx) in {1: (0.0, 260), 2: (t_rot, 60), 3: (t_l1, 90), 4: (t_l2, 90)}.items():
        f, x = entra(i, t0, dx)
        filtros.append(f)
        xs[i] = x
    filtros.append(f"[0:v][c1]overlay={xs[1]}:y=0[o1];[o1][c2]overlay={xs[2]}:y=0[o2];"
                   f"[o2][c3]overlay={xs[3]}:y=0[o3];[o3][c4]overlay={xs[4]}:y=0,format=yuv420p[v]")
    saida = CENAS / f"{nome}.mp4"
    ffmpeg("-i", fundo, *camada("gancho-painel"), *camada("gancho-rotulo"), *camada("gancho-linha1"),
           *camada("gancho-linha2"), "-filter_complex", ";".join(filtros), "-map", "[v]", "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, saida)
    return saida


# ---------- roteiro de cenas (início de cada uma, preso às falas) ----------
inicios = {
    "gancho": 0.0,
    "hoje": T["p3"] - 0.3,
    "solucao": T["s1"] - 0.3,
    "cel_ok": T["s2"] - 0.25,
    "cel_problema": T["i1"] - 0.45,
    "gestor": T["g1"] - 0.35,
    "mapa": T["g3"] - 0.25,
    "painel": T["g4"] - 0.25,
    "ia": T["a1"] - 0.4,
    "diferencial": T["d1"] - 0.3,
    "mapa_cinza": T["d2"] + 1.4,
    "fim": T["f1"] - 0.3,
}
ordem = list(inicios)
duracoes = {}
for i, nome in enumerate(ordem):
    prox = inicios[ordem[i + 1]] if i + 1 < len(ordem) else TOTAL
    duracoes[nome] = prox - inicios[nome] + (XF if i + 1 < len(ordem) else 0.0)


def cena(nome):
    d, ini = duracoes[nome], inicios[nome]
    print(f"cena {nome:13s} {ini:6.2f}s  dura {d:5.2f}s")
    if nome == "gancho":
        return render_gancho(nome, d)
    if nome == "hoje":
        troca = T["p4"] - ini - 0.2  # o segundo cartão acende quando a fala chega nele
        return render_cartela(nome, [("hoje-a", 0), ("hoje", troca)], d, 1.05, (1920, 1150))
    if nome == "solucao":
        return render_cartela(nome, [("solucao", 0)], d, 1.06)
    if nome == "diferencial":
        return render_cartela(nome, [("diferencial", 0)], d, 1.05, (2500, 1150))
    if nome == "fim":
        return render_cartela(nome, [("fim", 0)], d, 1.03)
    c, p = CEL, PC
    if nome == "cel_ok":
        botoes = centro_cel(c["zona_ok"]["botoes"], [24, 600, 732, 100])
        aviso = centro_cel(c["ok_registrado"]["aviso"], c["ok_registrado"]["cartao"])
        zona_mapa = centro_cel(c["mapa_cel"]["zona"])
        f = "fundo-cel-qr"
        return render_trechos(nome, [
            trecho("cel", m(c, "zona_ok") - 0.6, m(c, "zona_ok") + 2.6, fundo=f,
                   zoom=[(0, 1.0, 1120, 1080), (1.0, 1.0, 1120, 1080), (2.2, 1.7, *botoes)]),
            trecho("cel", m(c, "toque_ok") - 0.4, m(c, "ok_registrado") + 1.0, fundo=f, em=T["s4"] - 0.35,
                   zoom=fixo(1.7, aviso, de=(1.7, botoes), entra=0.6)),
            trecho("cel", m(c, "mapa_cel") - 0.1, m(c, "mapa_cel") + 2.8, fundo=f, em=T["s4"] + 1.0,
                   zoom=fixo(2.3, zona_mapa, de=(1.4, centro_cel(c["mapa_cel"]["svg"])), entra=0.8)),
        ], ini, d)
    if nome == "cel_problema":
        sug, ele = c["sugestao"], c["toque_eletrica"]
        duvida = centro_cel(sug["confianca"], sug["desempate"])
        risco = centro_cel(ele["alerta"], ele["prioridade"])
        texto = centro_cel([58, 420, 664, 330])
        return render_trechos(nome, [
            trecho("cel", m(c, "comeca_digitar") - 0.2, m(c, "digitou") + 0.4, fundo="fundo-cel-passo1",
                   zoom=fixo(1.7, texto)),
            trecho("cel", m(c, "digitou") + 0.4, m(c, "toque_sugestao") + 0.4, 1.3, fundo="fundo-cel-passo1",
                   zoom=fixo(1.7, texto)),
            trecho("cel", m(c, "sugestao") - 0.3, m(c, "toque_eletrica") - 0.45, fundo="fundo-cel-passo2",
                   em=T["i2"] - 0.3, zoom=fixo(1.85, duvida, de=(1.5, duvida), entra=0.6)),
            trecho("cel", m(c, "toque_eletrica") - 0.45, m(c, "toque_eletrica") + 1.2, fundo="fundo-cel-passo3",
                   em=T["i3"] - 0.45, zoom=fixo(1.85, duvida)),
            trecho("cel", m(c, "toque_eletrica") + 1.2, m(c, "toque_registrar") - 0.1, fundo="fundo-cel-passo4",
                   em=T["i4"] - 0.2, zoom=fixo(1.75, risco, de=(1.85, duvida), entra=0.7)),
            trecho("cel", m(c, "toque_registrar") - 0.1, m(c, "registrado") + 2.0, fundo="fundo-cel-passo4",
                   em=T["i5"] - 0.3, zoom=fixo(1.75, centro_cel(c["registrado"]["resultado"]), de=(1.75, risco))),
        ], ini, d)
    if nome == "gestor":
        prio = centro_pc(p["escolheu_p3"]["prioridade"], 420, 60)
        aviso = centro_pc(p["mantida"]["aviso"], 80, -60)
        lx, ly, lw, lh = p["mantida"]["linha"]
        perm = (lx + lw / 2, p["mantida"]["permanente"][1] + 420)  # coluna inteira + cabeçalho
        linha = centro_pc(p["mantida"]["linha"], 0, 40)
        mantem = T["g1"] + 0.55 * (E["g1"] - T["g1"])  # "...o sistema mantém P1"
        return render_trechos(nome, [
            trecho("pc", m(p, "escolheu_p3") - 0.6, m(p, "clicou_confirmar") + 0.25, 1.6, zoom=fixo(1.7, prio)),
            trecho("pc", m(p, "mantida") - 0.05, m(p, "mantida") + 1.8, em=mantem,
                   zoom=fixo(2.1, aviso, de=(1.7, aviso), entra=0.5)),
            trecho("pc", m(p, "mantida") + 1.8, m(p, "linha_tempo") + 1.6, em=T["g2"] - 0.2,
                   zoom=[(0, 1.75, *perm), (1.7, 1.75, *perm), (2.6, 1.6, *linha)]),
        ], ini, d)
    if nome == "mapa":
        cinzas = [centro_pc(cx) for cx in p["mapa_caixas"]["cinzas"]]
        mx = sum(x for x, _ in cinzas) / len(cinzas)
        my = sum(y for _, y in cinzas) / len(cinzas)
        return render_trechos(nome, [
            trecho("pc", m(p, "mapa") + 0.2, m(p, "mapa") + 4.8,
                   zoom=[(0, 1.4, 1300, 980), (d, 1.7, mx, my)]),
        ], ini, d)
    if nome == "painel":
        cab = p["painel"]["cabecalho"]  # "Indicadores por zona e por equipe. O sistema não avalia pessoas."
        return render_trechos(nome, [
            trecho("pc", m(p, "painel") + 0.1, m(p, "painel_fim") + 1.0,
                   zoom=[(0, 2.1, cab[0] + 716, cab[1] + 352), (d, 1.85, cab[0] + 806, cab[1] + 412)]),
        ], ini, d)
    if nome == "ia":
        tab = p["ia"]["tabela"]
        tabela = centro_pc(tab, 0, 150)
        campo = centro_pc(p["ia_campo"]["campo"], 0, 380)
        return render_trechos(nome, [
            trecho("pc", m(p, "ia") + 2.4, m(p, "ia_regras") + 1.6, zoom=fixo(1.65, tabela)),  # depois de a rolagem terminar
            trecho("pc", m(p, "ia_regras") + 1.6, m(p, "ia_modelo") + 1.0, em=T["a2"] - 0.8, zoom=fixo(1.65, tabela)),
            trecho("pc", m(p, "ia_campo") - 1.4, m(p, "ia_campo") + 3.0, em=T["a3"] - 0.6,
                   zoom=fixo(1.7, campo, de=(1.65, tabela), entra=1.2)),
        ], ini, d)
    if nome == "mapa_cinza":
        cinzas = [centro_pc(cx) for cx in p["mapa_caixas"]["cinzas"]]
        mx = sum(x for x, _ in cinzas) / len(cinzas)
        my = sum(y for _, y in cinzas) / len(cinzas)
        return render_trechos(nome, [
            trecho("pc", m(p, "mapa_caixas") + 0.5, m(p, "mapa_fim"), 1.4,
                   zoom=[(0, 1.45, mx, my), (d, 1.7, mx, my)]),
        ], ini, d)
    raise ValueError(nome)


# ---------- legendas (ASS) ----------
def tempo_ass(s):
    s = max(0.0, s)
    h, mi = int(s // 3600), int(s % 3600 // 60)
    return f"{h}:{mi:02d}:{s % 60:05.2f}"


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


SUB = r"\N{\fs32\b0}"
SECOES = [
    ("gancho", "1 · O PROBLEMA"),
    ("solucao", "2 · A SOLUÇÃO" + SUB + "no dia a dia"),
    ("cel_problema", "3 · FUNCIONALIDADES" + SUB + "IA com senso crítico"),
    ("gestor", "3 · FUNCIONALIDADES" + SUB + "supervisor e linha do tempo"),
    ("mapa", "3 · FUNCIONALIDADES" + SUB + "mapa ao vivo"),
    ("painel", "3 · FUNCIONALIDADES" + SUB + "painel por zona"),
    ("ia", "3 · FUNCIONALIDADES" + SUB + "o que medimos da IA"),
    ("diferencial", "4 · DIFERENCIAL"),
    ("fim", "5 · PRÓXIMO PASSO"),
]
CENAS_CEL = ("cel_ok", "cel_problema")
CENAS_CANTO = ("gancho", "gestor", "mapa", "painel", "ia", "mapa_cinza", "fim")  # rótulo no canto superior direito


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
Style: Baixo,Montserrat SemiBold,52,&H00FFFFFF,&H00FFFFFF,&H281B242C,&H00000000,0,0,0,0,100,100,0,0,3,16,0,2,150,150,40,1
Style: Lateral,Montserrat SemiBold,48,&H00FFFFFF,&H00FFFFFF,&H281B242C,&H00000000,0,0,0,0,100,100,0,0,3,16,0,2,1060,60,60,1
Style: Secao,Montserrat,45,&H00EFF4F6,&H00EFF4F6,&H00325C7A,&H00000000,-1,0,0,0,100,100,2,0,3,14,0,8,150,150,18,1
Style: SecaoCanto,Montserrat,45,&H00EFF4F6,&H00EFF4F6,&H00325C7A,&H00000000,-1,0,0,0,100,100,2,0,3,14,0,9,40,32,18,1
Style: SecaoLateral,Montserrat,45,&H00EFF4F6,&H00EFF4F6,&H00325C7A,&H00000000,-1,0,0,0,100,100,2,0,3,14,0,8,1060,60,18,1

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
            fim = TOTAL - 0.3
        lateral = cena_em(f["inicio"]) in CENAS_CEL
        estilo = "Lateral" if lateral else "Baixo"
        texto = quebrar(f["texto"], 28 if lateral else 52)
        linhas.append(f"Dialogue: 1,{tempo_ass(ini)},{tempo_ass(fim)},{estilo},,0,0,0,,{{\\fad(120,120)}}{texto}")
    # rótulo de seção: um por cena, no lugar que não cobre a tela
    for nome in ordem:
        rotulo = None
        for sec, r in SECOES:
            if inicios[sec] <= inicios[nome] + 1e-6:
                rotulo = r
        ini = inicios[nome] + (0.3 if nome != "gancho" else 0.2)
        fim = (inicios[ordem[ordem.index(nome) + 1]] if nome != ordem[-1] else TOTAL) - 0.05
        estilo = "SecaoLateral" if nome in CENAS_CEL else "SecaoCanto" if nome in CENAS_CANTO else "Secao"
        linhas.append(f"Dialogue: 0,{tempo_ass(ini)},{tempo_ass(fim)},{estilo},,0,0,0,,{{\\fad(150,150)}}{rotulo}")
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
    marca.update(json.dumps([inicios, TOTAL, T]).encode())
    assinatura = CENAS / "base.assinatura"
    if base.exists() and assinatura.exists() and assinatura.read_text() == marca.hexdigest():
        print("imagens iguais às da última montagem: reaproveitando a base")
        return finalizar(base)
    arquivos = [cena(n) for n in ordem]
    entradas, filtros = [], []
    for a in arquivos:
        entradas += ["-i", a]
    atual = "[0:v]"
    for i in range(1, len(arquivos)):
        dur_xf = 0.04 if ordem[i] in CORTE_SECO else XF
        filtros.append(f"{atual}[{i}:v]xfade=transition=fade:duration={dur_xf}:offset={inicios[ordem[i]]:.3f}[x{i}]")
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
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-maxrate", "4000k", "-bufsize", "8000k",
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", FPS,
           "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-ar", "48000",
           "-t", f"{TOTAL:.3f}", "-movflags", "+faststart", SAIDA)
    print(f"pronto: {SAIDA} ({TOTAL:.1f} s)")


if __name__ == "__main__":
    montar()
