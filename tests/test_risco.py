"""Testa palavras de risco. Dono: IA (tarefa #7)."""
import pytest

from ia.modelo import sugerir
from ia.risco import detectar_risco


@pytest.mark.skip(reason="tarefa #7: apague esta linha quando implementar detectar_risco")
@pytest.mark.parametrize("texto", ["Fumaça saindo da cozinha", "cheiro de FOGO", "funcionário levou choque"])
def test_detecta_risco(texto):
    assert detectar_risco(texto)


def test_texto_comum_sem_risco():
    assert not detectar_risco("falta papel higiênico")


def test_sugestao_tem_formato_do_contrato():
    s = sugerir("vaso entupido")
    assert set(s) == {"categoria", "prioridade", "equipe", "confianca", "risco", "aviso"}
