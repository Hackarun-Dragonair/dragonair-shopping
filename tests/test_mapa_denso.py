"""Mapa denso: as dezenas de lojas fictícias são geradas por funções curtas, não desenhadas à mão."""
from pathlib import Path

MAPA_JS = Path(__file__).resolve().parent.parent / "app" / "static" / "js" / "mapa.js"


def test_lojas_saem_de_funcoes_de_fileira_e_leque():
    texto = MAPA_JS.read_text(encoding="utf-8")
    assert "function fileira(" in texto
    assert "function leque(" in texto
    # Térreo, L1 e L2 têm lojas de fundo; o estacionamento tem vagas
    assert texto.count("lojas: [") >= 3
    assert "vagas(" in texto
