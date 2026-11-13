"""Testa palavras de risco. Dono: IA (tarefa #7)."""
import pytest

from ia.modelo import sugerir
from ia.risco import AVISO_BRIGADA, detectar_risco


@pytest.mark.parametrize("texto", [
    "Fumaça saindo da cozinha", "cheiro de FOGO", "funcionário levou choque",
    "fumaca no corredor", "tomada soltando faísca", "pessoa presa no elevador",
])
def test_detecta_risco(texto):
    assert detectar_risco(texto)


@pytest.mark.parametrize("texto", ["falta papel higiênico", "lixeira cheia", "", "lâmpada queimada"])
def test_texto_comum_sem_risco(texto):
    assert not detectar_risco(texto)


def test_sugestao_tem_formato_do_contrato():
    s = sugerir("vaso entupido")
    assert set(s) == {"categoria", "prioridade", "equipe", "confianca", "risco", "aviso"}


def test_risco_sempre_urgente_com_aviso():
    s = sugerir("fumaça saindo da cozinha")
    assert s["risco"] is True
    assert s["prioridade"] == "urgente"
    assert s["aviso"] == AVISO_BRIGADA


def test_tela_sobre_ia_mostra_acerto():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as cliente:
        r = cliente.get("/sobre-modelo")
    assert r.status_code == 200 and "Quanto ela acerta" in r.text
