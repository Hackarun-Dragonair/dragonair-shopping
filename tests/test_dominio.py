from datetime import datetime, timedelta, timezone

import pytest

from app.dominio import (
    AVISO_BRIGADA,
    Previsao,
    detectar_risco,
    escolher_categoria,
    estado_da_zona,
    garantir_prioridade,
    triar,
)

AGORA = datetime(2026, 11, 13, 15, 0, tzinfo=timezone.utc)


def test_palavras_de_risco_disparam_o_aviso():
    for frase in (
        "tem fumaça na praça",
        "vi fogo na lixeira",
        "tomada deu choque",
        "pessoa presa no elevador",
        "incêndio no corredor",
    ):
        assert detectar_risco(frase)


def test_piso_molhado_nao_e_risco_de_brigada():
    assert not detectar_risco("piso molhado sem placa")
    assert not detectar_risco("fogão da lanchonete sujo")


def test_risco_nao_rebaixa_mesmo_se_o_modelo_disser_p4():
    sugestao = triar(
        "tem fumaça na praça de alimentação",
        Previsao("limpeza", 0.9, None, None, "P4"),
    )
    assert sugestao.prioridade == "P1"
    assert sugestao.risco is True
    assert sugestao.aviso == AVISO_BRIGADA


def test_edicao_com_risco_volta_para_p1():
    prioridade, risco = garantir_prioridade("pessoa presa no elevador", "P3")
    assert prioridade == "P1"
    assert risco is True


def test_duvida_mostra_as_duas_categorias():
    categoria, confianca, alternativa, _alt = escolher_categoria(
        [("hidraulica", 0.42), ("climatizacao", 0.36), ("limpeza", 0.1)]
    )
    assert categoria == "hidraulica"
    assert alternativa == "climatizacao"
    assert confianca == pytest.approx(0.42)


def test_categoria_folgada_nao_pede_desempate():
    _categoria, _conf, alternativa, _alt = escolher_categoria(
        [("hidraulica", 0.8), ("eletrica", 0.1)]
    )
    assert alternativa is None


def test_zona_fica_cinza_quando_o_prazo_vence():
    estado = estado_da_zona(
        ultimo_resultado="ok",
        ultima_em=AGORA - timedelta(minutes=61),
        prazo_minutos=60,
        problema_aberto=False,
        agora=AGORA,
    )
    assert estado == "cinza"


def test_problema_aberto_nao_fica_cinza():
    estado = estado_da_zona(
        ultimo_resultado="problema",
        ultima_em=AGORA - timedelta(hours=5),
        prazo_minutos=60,
        problema_aberto=True,
        agora=AGORA,
    )
    assert estado == "problema"


def test_zona_sem_conferencia_fica_cinza():
    estado = estado_da_zona(
        ultimo_resultado=None,
        ultima_em=None,
        prazo_minutos=60,
        problema_aberto=False,
        agora=AGORA,
    )
    assert estado == "cinza"
