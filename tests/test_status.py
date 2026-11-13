"""Testa a cor das zonas. Dono: DADOS + TELAS."""
from datetime import datetime

from app.status import cor_da_zona

AGORA = datetime(2026, 11, 13, 20, 0)


def test_nunca_conferida_fica_cinza():
    assert cor_da_zona(None, None, 60, AGORA) == "cinza"


def test_dentro_do_prazo():
    assert cor_da_zona("problema", "2026-11-13T19:30:00", 60, AGORA) == "vermelho"


def test_passou_do_prazo_fica_cinza():
    assert cor_da_zona("ok", "2026-11-13T18:00:00", 60, AGORA) == "cinza"
