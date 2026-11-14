"""Renderiza as cartelas (cartelas.html) em PNG 3840x2160 (o dobro de 1920x1080, para o zoom suave).

Uso: <python com playwright>/bin/python docs/pitch/video/render_cartelas.py <pasta_trabalho> <qr.svg>
Precisa das fontes Montserrat em <pasta_trabalho>/fontes (licença OFL, baixadas pelo fazer_video.sh).
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
trabalho = Path(sys.argv[1]).resolve()
qr = Path(sys.argv[2]).read_text()
if "viewBox" not in qr:  # o segno grava largura fixa; com viewBox o QR estica no tamanho da etiqueta
    import re
    m = re.search(r'width="(\d+)" height="(\d+)"', qr)
    qr = qr.replace(m.group(0), f'viewBox="0 0 {m.group(1)} {m.group(2)}"', 1)
saida = trabalho / "cartelas"
saida.mkdir(parents=True, exist_ok=True)

# Passos da cena do celular: um fundo para cada passo em destaque.
PASSOS = [
    ("Toca Problema e escreve do seu jeito", ""),
    ("A IA sugere categoria e prioridade", ""),
    ("Em dúvida, ela pergunta. A pessoa decide", ""),
    ("Risco: P1 e aviso para a brigada", "risco"),
]
blocos = []
for atual in range(1, len(PASSOS) + 1):
    itens = []
    for i, (texto, extra) in enumerate(PASSOS, start=1):
        estado = "feito" if i < atual else "agora" if i == atual else ""
        itens.append(f'<li class="{estado} {extra}"><i>{i}</i>{texto}</li>')
    blocos.append(f'''<section id="fundo-cel-passo{atual}" class="fundo-cel"><div class="halo"></div>
  <div class="coluna"><div class="rotulo">No celular do funcionário</div><ul class="passos">{"".join(itens)}</ul></div></section>''')

html = (AQUI / "cartelas.html").read_text()
html = html.replace("{{FONTES}}", (trabalho / "fontes").as_uri()).replace("{{QR}}", qr).replace("{{PASSOS}}", "\n".join(blocos))
pagina = trabalho / "cartelas.html"
pagina.write_text(html)

with sync_playwright() as p:
    nav = p.chromium.launch(channel="chrome")
    page = nav.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
    page.goto(pagina.as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(500)
    for secao in page.locator("section").all():
        nome = secao.get_attribute("id")
        secao.screenshot(path=str(saida / f"{nome}.png"), omit_background=True)
        print("cartela:", nome)
    nav.close()
