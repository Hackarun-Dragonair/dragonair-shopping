"""Cenário fictício de um shopping. Nenhum dado é de pessoa real.

Crachás ficam gravados para o S2 (celular autorizado). A demo entra
pelo usuário fictício, sem pedir crachá.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta

from app.consultas import agora_utc
from app.db import instalar_triggers
from app.servico import abrir_problema, assumir_problema, registrar_conferencia, resolver_problema

EQUIPES = (
    ("manutencao", "Manutenção"),
    ("limpeza", "Limpeza"),
    ("seguranca", "Segurança"),
    ("climatizacao", "Climatização"),
)

USUARIOS = (
    ("rita", "Rita Melo", "encarregado", "Encarregada", None),
    ("otto", "Otto Lima", "supervisor", "Supervisor", None),
    ("lia", "Lia Prado", "coordenacao", "Coordenação", None),
    ("caio", "Caio Nunes", "manutencao", "Manutenção", "manutencao"),
)

ENCAMINHAMENTO = (
    ("hidraulica", "manutencao"),
    ("eletrica", "manutencao"),
    ("estrutura", "manutencao"),
    ("climatizacao", "climatizacao"),
    ("limpeza", "limpeza"),
    ("seguranca", "seguranca"),
)

ZONAS = (
    ("sanitario-piso1", "Sanitário piso 1", "sanitario", "L1", 1, 60, "Placa de aviso no corredor dos banheiros"),
    ("entrada-principal", "Entrada principal", "entrada", "Térreo", 0, 120, "Lado de dentro, junto à porta"),
    ("praca-a", "Praça de alimentação — setor A", "praca_alimentacao", "L1", 1, 90, "Pilar do contorno, setor A"),
    ("praca-b", "Praça de alimentação — setor B", "praca_alimentacao", "L1", 1, 90, "Pilar do contorno, setor B"),
    ("banheiro-l1-sul", "Banheiro L1 sul", "sanitario", "L1", 1, 60, "Placa de aviso no corredor dos banheiros"),
    ("corredor-norte", "Corredor mall norte", "corredor", "L1", 1, 120, "Placa de identificação no início do corredor"),
    ("escada-norte", "Escada rolante norte", "escada", "L1", 1, 180, "Painel lateral na base"),
    ("banheiro-l2-norte", "Banheiro L2 norte", "sanitario", "L2", 2, 60, "Placa de aviso no corredor dos banheiros"),
    ("area-tecnica-l2", "Área técnica L2", "area_tecnica", "L2", 2, 240, "Placa da porta, corredor de serviço"),
    ("doca-1", "Doca 1", "doca", "Térreo", 0, 180, "Placa de identificação da doca"),
    ("estacionamento-g1", "Estacionamento G1", "estacionamento", "Estacionamento", 3, 180, "Coluna numerada da garagem"),
)


def _limpar(conn: sqlite3.Connection) -> None:
    # A trava da linha do tempo bloqueia DELETE no uso normal.
    # O recomeço do cenário fictício tira a trava, apaga e coloca de volta.
    conn.execute("DROP TRIGGER IF EXISTS eventos_sem_delete")
    conn.execute("DROP TRIGGER IF EXISTS eventos_sem_update")
    for tabela in (
        "leituras",
        "eventos",
        "problemas",
        "conferencias",
        "crachas",
        "dispositivos",
        "encaminhamento",
        "usuarios",
        "zonas",
        "equipes",
    ):
        conn.execute(f"DELETE FROM {tabela}")
    instalar_triggers(conn)


def _id(conn: sqlite3.Connection, tabela: str, codigo: str) -> int:
    return conn.execute(
        f"SELECT id FROM {tabela} WHERE codigo = ?", (codigo,)
    ).fetchone()["id"]


def _usuario(conn: sqlite3.Connection, codigo: str) -> dict:
    return dict(
        conn.execute("SELECT * FROM usuarios WHERE codigo = ?", (codigo,)).fetchone()
    )


def semear(conn: sqlite3.Connection, agora: datetime | None = None) -> None:
    agora = agora or agora_utc()
    with conn:
        _limpar(conn)
        for codigo, nome in EQUIPES:
            conn.execute(
                "INSERT INTO equipes (codigo, nome) VALUES (?, ?)", (codigo, nome)
            )
        for codigo, nome, papel, funcao, equipe in USUARIOS:
            equipe_id = _id(conn, "equipes", equipe) if equipe else None
            conn.execute(
                """
                INSERT INTO usuarios (codigo, nome, papel, funcao, equipe_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (codigo, nome, papel, funcao, equipe_id),
            )
            conn.execute(
                "INSERT INTO crachas (codigo, usuario_id, ativo) VALUES (?, ?, 1)",
                (codigo.upper(), conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]),
            )
        for categoria, equipe in ENCAMINHAMENTO:
            conn.execute(
                "INSERT INTO encaminhamento (categoria, equipe_id) VALUES (?, ?)",
                (categoria, _id(conn, "equipes", equipe)),
            )
        for zona in ZONAS:
            conn.execute(
                """
                INSERT INTO zonas (
                  codigo, nome, tipo, piso, ordem_piso, prazo_minutos, local_qr
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                zona,
            )
        _cenario(conn, agora)


def _conferir(conn, zona: str, resultado: str, quem: str, no_local: bool, quando: datetime) -> None:
    registrar_conferencia(
        conn,
        zona_id=_id(conn, "zonas", zona),
        resultado=resultado,
        usuario_id=_id(conn, "usuarios", quem),
        no_local=no_local,
        agora=quando,
    )


def _problema_resolvido(conn, zona, quem, descricao, categoria, prioridade, equipe, inicio, minutos) -> None:
    usuario = _usuario(conn, quem)
    equipe_id = _id(conn, "equipes", equipe)
    problema_id = abrir_problema(
        conn,
        zona_id=_id(conn, "zonas", zona),
        usuario=usuario,
        descricao=descricao,
        perto_de="",
        origem="qr",
        categoria=categoria,
        prioridade=prioridade,
        equipe_id=equipe_id,
        sugestao_categoria=categoria,
        sugestao_prioridade=prioridade,
        sugestao_equipe_id=equipe_id,
        risco=False,
        agora=inicio,
    )
    assumir_problema(
        conn,
        problema_id=problema_id,
        usuario=_usuario(conn, "caio"),
        agora=inicio + timedelta(minutes=10),
    )
    resolver_problema(
        conn,
        problema_id=problema_id,
        usuario=_usuario(conn, "caio"),
        agora=inicio + timedelta(minutes=minutos),
    )


def _cenario(conn: sqlite3.Connection, agora: datetime) -> None:
    # Banheiro L2 conferido agora, com duas limpezas na semana (reincidência).
    _problema_resolvido(
        conn, "banheiro-l2-norte", "rita",
        "Piso molhado sem placa", "limpeza", "P2", "limpeza",
        agora - timedelta(days=5), 50,
    )
    _problema_resolvido(
        conn, "banheiro-l2-norte", "rita",
        "Sem papel e mau cheiro", "limpeza", "P3", "limpeza",
        agora - timedelta(days=1, hours=3), 35,
    )
    _conferir(conn, "banheiro-l2-norte", "ok", "rita", True, agora - timedelta(minutes=12))

    # Conferido fora do prazo: fica cinza.
    _conferir(conn, "banheiro-l1-sul", "ok", "rita", True, agora - timedelta(hours=3))

    # Atenção recente na praça B.
    _conferir(conn, "praca-b", "atencao", "rita", True, agora - timedelta(minutes=18))

    # Problema aberto no corredor, ainda sem confirmação do supervisor.
    rita = _usuario(conn, "rita")
    manutencao = _id(conn, "equipes", "manutencao")
    abrir_problema(
        conn,
        zona_id=_id(conn, "zonas", "corredor-norte"),
        usuario=rita,
        descricao="Lâmpada queimada no começo do corredor",
        perto_de="teto",
        origem="qr",
        categoria="eletrica",
        prioridade="P3",
        equipe_id=manutencao,
        sugestao_categoria="eletrica",
        sugestao_prioridade="P3",
        sugestao_equipe_id=manutencao,
        risco=False,
        agora=agora - timedelta(minutes=25),
    )

    _conferir(conn, "escada-norte", "ok", "rita", True, agora - timedelta(minutes=8))
    _conferir(conn, "entrada-principal", "ok", "rita", True, agora - timedelta(minutes=40))
    _conferir(conn, "area-tecnica-l2", "ok", "caio", True, agora - timedelta(minutes=30))
    # praca-a, doca-1 e estacionamento-g1 ficam sem conferência (cinza).
