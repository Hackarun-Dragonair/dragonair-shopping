"""Desenho fictício do mapa: cobre todas as zonas e não usa nomes de lojas reais."""
from pathlib import Path

from app.seed import ZONAS

MAPA_JS = Path(__file__).resolve().parent.parent / "app" / "static" / "js" / "mapa.js"

# Nomes de marcas reais que NÃO podem aparecer no desenho (a planta do shopping é dado sensível)
MARCAS_REAIS = ["renner", "c&a", "rchlo", "riachuelo", "outback", "mcdonald", "spoleto"]


def _texto_do_mapa():
    return MAPA_JS.read_text(encoding="utf-8")


def test_pagina_inicial_carrega_o_mapa(client):
    html = client.get("/").get_data(as_text=True)
    assert "js/mapa.js" in html
    assert 'id="mapa-caixa"' in html


def test_desenho_tem_as_11_zonas_do_seed():
    texto = _texto_do_mapa()
    codigos = [zona[0] for zona in ZONAS]
    assert len(codigos) == 11
    faltando = [c for c in codigos if f'"{c}"' not in texto]
    assert faltando == []


def test_desenho_aceita_poligono_e_avisa_que_e_ficticio():
    texto = _texto_do_mapa()
    assert "pts:" in texto  # zonas em polígono (formas irregulares)
    assert "Desenho fictício feito do zero pela equipe" in texto


def test_desenho_nao_usa_nomes_de_marcas_reais():
    texto = _texto_do_mapa().lower()
    encontradas = [m for m in MARCAS_REAIS if m in texto]
    assert encontradas == []
