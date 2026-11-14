"""Grava a tela do app de verdade (celular e computador) para o vídeo do pitch.

Uso: <python com playwright>/bin/python docs/pitch/video/gravar_telas.py <pasta_saida> [url_base]
Precisa do servidor ligado (servidor_gravacao.py, porta 8778) com o banco recém-semeado.

Como funciona:
  - abre o Chrome sem janela e grava quadro a quadro pelo "screencast" do próprio Chrome
    (JPEG de alta qualidade, cada quadro com a hora exata);
  - faz os cliques da demo (docs/pitch/demo-cliques.md) com o mouse andando devagar;
  - SÓ durante a gravação, injeta uma seta de mouse e um círculo de toque desenhados em CSS,
    porque o Chrome sem janela não desenha o cursor;
  - guarda marcas de tempo (marcas.json) para a montagem cortar as esperas.
Saída: celular.mp4 (780x1688), computador.mp4 (3072x1728, tela de 1536x864 com zoom 2x) e marcas.json.
"""
import asyncio
import base64
import json
import math
import subprocess
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright

SAIDA = Path(sys.argv[1])
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8778"
SAIDA.mkdir(parents=True, exist_ok=True)

# Seta do mouse e círculo de clique/toque: só existem na gravação, não no app.
CURSOR_JS = r"""
(() => {
  const instalar = () => {
    if (document.getElementById('__cursor')) return;
    const css = document.createElement('style');
    css.textContent = `
      #__cursor { position: fixed; left: 0; top: 0; width: 26px; height: 26px; z-index: 2147483647;
        pointer-events: none; transform: translate(-100px, -100px); transition: none; }
      .__toque { position: fixed; z-index: 2147483646; pointer-events: none; border-radius: 50%;
        width: 54px; height: 54px; margin: -27px 0 0 -27px; background: rgba(122,92,50,.30);
        border: 3px solid rgba(122,92,50,.85); animation: __toque .65s ease-out forwards; }
      @keyframes __toque { from { transform: scale(.35); opacity: 1; } to { transform: scale(1.25); opacity: 0; } }
      html { scrollbar-width: none; } ::-webkit-scrollbar { display: none; }`;
    document.head.appendChild(css);
    const c = document.createElement('div');
    c.id = '__cursor';
    c.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2 L4 19 L8.6 14.8 L11.6 21.4 L14.4 20.2 L11.4 13.7 L17.6 13.7 Z"
      fill="#fff" stroke="#2c241b" stroke-width="1.6" stroke-linejoin="round"/></svg>`;
    if (!window.__semCursor) document.body.appendChild(c);
    let xy = window.__ultimoXY;
    try { xy = xy || JSON.parse(sessionStorage.getItem('__xy')); } catch (e) { /* sem storage */ }
    if (xy) c.style.transform = `translate(${xy[0]}px, ${xy[1]}px)`;
  };
  const toque = (x, y) => {
    const t = document.createElement('div'); t.className = '__toque';
    t.style.left = x + 'px'; t.style.top = y + 'px';
    document.body.appendChild(t); setTimeout(() => t.remove(), 700);
  };
  window.__toque = toque;
  addEventListener('mousemove', e => {
    window.__ultimoXY = [e.clientX, e.clientY];
    try { sessionStorage.setItem('__xy', JSON.stringify(window.__ultimoXY)); } catch (er) { /* sem storage */ }
    const c = document.getElementById('__cursor');
    if (c) c.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
  }, true);
  addEventListener('mousedown', e => toque(e.clientX, e.clientY), true);
  addEventListener('touchstart', e => { for (const p of e.touches) toque(p.clientX, p.clientY); }, true);
  if (document.readyState === 'loading') addEventListener('DOMContentLoaded', instalar); else instalar();
})();
"""


class Gravador:
    """Recebe os quadros do screencast do Chrome e guarda com a hora de cada um."""

    def __init__(self, page, nome, largura, altura):
        self.page, self.nome, self.largura, self.altura = page, nome, largura, altura
        self.pasta = SAIDA / f"quadros-{nome}"
        self.pasta.mkdir(exist_ok=True)
        for velho in self.pasta.glob("*.jpg"):
            velho.unlink()
        self.quadros = []  # (hora, arquivo)
        self.marcas = {}
        self.inicio = None

    async def comecar(self):
        self.cdp = await self.page.context.new_cdp_session(self.page)
        self.cdp.on("Page.screencastFrame", self._quadro)
        await self.cdp.send("Page.startScreencast", {
            "format": "jpeg", "quality": 92, "maxWidth": self.largura, "maxHeight": self.altura, "everyNthFrame": 1})
        await asyncio.sleep(0.6)

    def _quadro(self, ev):
        hora = ev["metadata"]["timestamp"]
        arq = self.pasta / f"{len(self.quadros):05d}.jpg"
        arq.write_bytes(base64.b64decode(ev["data"]))
        self.quadros.append((hora, arq.name))
        if self.inicio is None:
            self.inicio = hora
        asyncio.ensure_future(self.cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]}))

    def marcar(self, nome, **extra):
        agora = time.time()
        self.marcas[nome] = dict(t=round(agora - (self.inicio or agora), 3), **extra)
        print(f"  [{self.nome}] {self.marcas[nome]['t']:6.2f}s {nome}")

    async def caixa(self, seletor):
        """Retângulo do elemento em pixels do vídeo (para o zoom da montagem)."""
        b = await self.page.locator(seletor).first.bounding_box()
        escala = self.largura / self.page.viewport_size["width"]
        return [round(v * escala) for v in (b["x"], b["y"], b["width"], b["height"])]

    async def parar(self):
        await asyncio.sleep(0.5)
        await self.cdp.send("Page.stopScreencast")
        fim = time.time()
        lista = SAIDA / f"lista-{self.nome}.txt"
        linhas = ["ffconcat version 1.0"]
        for i, (hora, arq) in enumerate(self.quadros):
            prox = self.quadros[i + 1][0] if i + 1 < len(self.quadros) else fim
            linhas += [f"file '{self.pasta / arq}'", f"duration {max(prox - hora, 0.001):.4f}"]
        linhas.append(f"file '{self.pasta / self.quadros[-1][1]}'")
        lista.write_text("\n".join(linhas) + "\n")
        video = SAIDA / f"{self.nome}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                        "-vf", f"fps=30,scale={self.largura}:{self.altura}:flags=lanczos,format=yuv420p",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "12", str(video)], check=True)
        print(f"  [{self.nome}] {len(self.quadros)} quadros → {video}")
        return self.marcas


async def mover(page, x, y, duracao=0.9):
    """Move o mouse com aceleração suave (começa e termina devagar), como uma mão de verdade."""
    x0, y0 = getattr(page, "_xy", (page.viewport_size["width"] * 0.6, page.viewport_size["height"] * 0.7))
    passos = max(8, int(duracao * 60))
    curva = (x - x0) * 0.08  # leve arco, para não parecer robô
    for i in range(1, passos + 1):
        s = i / passos
        e = s * s * (3 - 2 * s)
        await page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e - math.sin(math.pi * s) * curva * 0.5)
        await asyncio.sleep(duracao / passos)
    page._xy = (x, y)


async def ir_ate(page, seletor, duracao=0.9, dx=0.5, dy=0.5):
    b = await page.locator(seletor).first.bounding_box()
    x, y = b["x"] + b["width"] * dx, b["y"] + b["height"] * dy
    await mover(page, x, y, duracao)
    return x, y


async def clicar(page, seletor, duracao=0.9, espera=0.25):
    await ir_ate(page, seletor, duracao)
    await asyncio.sleep(espera)
    await page.mouse.down()
    await asyncio.sleep(0.08)
    await page.mouse.up()


async def rolar_ate(page, seletor, topo=90, duracao=0.9):
    """Rola a página suavemente até o elemento ficar perto do topo."""
    y = await page.evaluate(f"""(t) => {{ const e = document.querySelector({json.dumps(seletor)});
        return e.getBoundingClientRect().top + scrollY - t; }}""", topo)
    y0 = await page.evaluate("scrollY")
    comeco = time.time()
    while True:  # cada passo leva o tempo que levar; a posição segue o relógio
        s = min(1.0, (time.time() - comeco) / duracao)
        await page.evaluate(f"scrollTo(0, {y0 + (y - y0) * s * s * (3 - 2 * s)})")
        if s >= 1.0:
            break
        await asyncio.sleep(0.01)


async def tocar(page, seletor):
    await page.locator(seletor).first.scroll_into_view_if_needed()
    await page.tap(seletor)


async def celular(nav):
    print("celular (funcionário, sem crachá)")
    ctx = await nav.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                                is_mobile=True, has_touch=True, locale="pt-BR")
    await ctx.add_init_script("window.__semCursor = true;" + CURSOR_JS)
    page = await ctx.new_page()
    await page.goto(BASE + "/telas/fila")  # aquece o servidor (primeiro acesso)
    await page.goto("about:blank")
    g = Gravador(page, "celular", 780, 1688)
    await g.comecar()
    await page.goto(BASE + "/z/area-tecnica-l2?origem=qr")
    await page.wait_for_load_state("networkidle")
    g.marcar("zona")
    await asyncio.sleep(3.0)
    await page.tap("#botao-problema")
    g.marcar("toque_problema")
    await page.wait_for_selector(".atalho")
    await asyncio.sleep(1.2)  # o próprio app rola até o formulário
    await rolar_ate(page, "#painel-problema", topo=70, duracao=0.6)
    g.marcar("painel_problema")
    await asyncio.sleep(1.0)
    await page.tap("#descricao")
    g.marcar("comeca_digitar")
    await page.locator("#descricao").press_sequentially("cheiro de fumaça no quadro", delay=85)
    g.marcar("digitou")
    await asyncio.sleep(0.5)
    await page.tap("#perto")
    await page.select_option("#perto", "quadro")
    await asyncio.sleep(0.8)
    await page.tap("#botao-sugestao")
    g.marcar("toque_sugestao")
    await page.wait_for_selector("#sugestao:not(.d-none)")
    await asyncio.sleep(0.4)
    await rolar_ate(page, "#sugestao", topo=72, duracao=1.0)
    await asyncio.sleep(0.3)
    g.marcar("sugestao", alerta=await g.caixa("#alerta-risco"), desempate=await g.caixa("#desempate"),
             prioridade=await g.caixa("#prioridade"))
    await asyncio.sleep(3.5)
    eletrica = "#desempate button:has-text('Elétrica')"
    await page.tap(eletrica)
    g.marcar("toque_eletrica", categoria=await g.caixa("#categoria"))
    await asyncio.sleep(2.0)
    await page.tap("#botao-registrar")
    g.marcar("toque_registrar")
    await page.wait_for_selector("#resultado a")
    await asyncio.sleep(0.4)
    await rolar_ate(page, "#resultado", topo=260, duracao=0.9)
    g.marcar("registrado", resultado=await g.caixa("#resultado"))
    await asyncio.sleep(3.0)
    marcas = await g.parar()
    href = await page.locator("#resultado a").first.get_attribute("href")
    await ctx.close()
    return marcas, href


async def computador(nav, href):
    print("computador (gestor OTTO)")
    ctx = await nav.new_context(viewport={"width": 1536, "height": 864}, device_scale_factor=2, locale="pt-BR")
    await ctx.add_init_script(CURSOR_JS)
    page = await ctx.new_page()
    # Entrar como gestor OTTO (fictício) antes de gravar; o login não aparece no vídeo.
    await page.goto(BASE + "/entrar")
    await page.locator("form:has(input[value='OTTO']) button").click()
    await page.wait_for_load_state()
    await page.goto(BASE + "/telas/fila")
    await page.wait_for_load_state("networkidle")
    page._xy = (1100, 640)
    await page.mouse.move(1100, 640)
    g = Gravador(page, "computador", 3072, 1728)  # 2x: dá zoom na montagem sem borrar
    await g.comecar()
    cartao = f"a.cartao[href='{href}']"
    g.marcar("fila", cartao=await g.caixa(cartao))
    await asyncio.sleep(1.2)
    await ir_ate(page, cartao, 1.2, dx=0.4, dy=0.45)
    await asyncio.sleep(0.6)
    await clicar(page, cartao, 0.3, espera=0.1)
    await page.wait_for_load_state("networkidle")
    g.marcar("problema")
    await asyncio.sleep(1.2)
    await clicar(page, "#prioridade", 1.0)
    await page.select_option("#prioridade", "P3")
    g.marcar("escolheu_p3", prioridade=await g.caixa("#prioridade"))
    await asyncio.sleep(1.0)
    await clicar(page, "[data-acao=confirmar]", 0.9)
    g.marcar("clicou_confirmar")
    await page.wait_for_selector("#mensagem .aviso")
    await page.wait_for_load_state("networkidle")
    g.marcar("mantida", aviso=await g.caixa("#mensagem .aviso"), linha=await g.caixa(".linha-tempo"))
    await asyncio.sleep(2.5)
    await ir_ate(page, ".linha-tempo li:last-child", 1.4, dx=0.3)
    g.marcar("linha_tempo")
    await asyncio.sleep(3.0)

    await page.goto(BASE + "/")
    await page.wait_for_selector("svg .zona")
    await asyncio.sleep(0.8)
    g.marcar("mapa")
    await asyncio.sleep(1.0)
    cinzas = page.locator("svg .zona.z-cinza")
    n = await cinzas.count()
    print("  zonas cinza no mapa:", n)
    g.marcar("mapa_caixas", svg=await g.caixa("svg.mapa-svg"), cinzas=[await g.caixa(f"svg .zona.z-cinza >> nth={i}") for i in range(n)])
    alvos = [await cinzas.nth(i).bounding_box() for i in range(min(n, 3))]
    for b in alvos:
        if b:
            await mover(page, b["x"] + b["width"] * 0.5, b["y"] + b["height"] * 0.55, 1.1)
            await asyncio.sleep(0.9)
    g.marcar("mapa_fim")
    await asyncio.sleep(1.0)

    await page.goto(BASE + "/telas/painel")
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(0.6)
    g.marcar("painel", topo=await g.caixa("main .row >> nth=0"))
    await mover(page, 760, 300, 1.4)
    await asyncio.sleep(2.0)
    await page.mouse.wheel(0, 0)
    g.marcar("painel_fim")
    await asyncio.sleep(1.5)

    await page.goto(BASE + "/telas/sobre-a-ia")
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(0.6)
    g.marcar("ia", numeros=await g.caixa(".row, .cartoes-ia, main .card"))
    await asyncio.sleep(1.0)
    await ir_ate(page, "text=dos P1 marcados como P1", 1.4)
    g.marcar("ia_p1")
    await asyncio.sleep(2.5)
    await ir_ate(page, "text=Modelo + regra dura >> nth=-1", 1.2)
    g.marcar("ia_tabela", tabela=await g.caixa("table >> nth=0"))
    await asyncio.sleep(3.5)
    marcas = await g.parar()
    await ctx.close()
    return marcas


async def principal():
    async with async_playwright() as p:
        nav = await p.chromium.launch(channel="chrome")
        m_cel, href = await celular(nav)
        m_pc = await computador(nav, href)
        await nav.close()
    (SAIDA / "marcas.json").write_text(json.dumps({"celular": m_cel, "computador": m_pc}, indent=1, ensure_ascii=False))


asyncio.run(principal())
