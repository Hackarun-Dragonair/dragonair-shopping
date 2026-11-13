"""Grava conferência, problema e eventos. Evento não tem função de apagar."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from app.consultas import equipe_da_categoria, iso
from app.dominio import nome_categoria

PERTO_DE_NOME = {
    "saida_de_ar": "saída de ar",
    "cano": "cano",
    "quadro": "quadro",
    "teto": "teto",
    "outro": "outro",
}


def acrescentar_evento(
    conn: sqlite3.Connection,
    problema_id: int,
    tipo: str,
    texto: str,
    papel: str,
    agora: datetime,
) -> None:
    conn.execute(
        """
        INSERT INTO eventos (problema_id, tipo, texto, papel, criado_em)
        VALUES (?, ?, ?, ?, ?)
        """,
        (problema_id, tipo, texto, papel, iso(agora)),
    )


def registrar_conferencia(
    conn: sqlite3.Connection,
    *,
    zona_id: int,
    resultado: str,
    usuario_id: int,
    no_local: bool,
    agora: datetime,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO conferencias (zona_id, resultado, usuario_id, no_local, criado_em)
        VALUES (?, ?, ?, ?, ?)
        """,
        (zona_id, resultado, usuario_id, 1 if no_local else 0, iso(agora)),
    )
    return int(cursor.lastrowid)


def abrir_problema(
    conn: sqlite3.Connection,
    *,
    zona_id: int,
    usuario: dict,
    descricao: str,
    perto_de: str,
    origem: str,
    categoria: str,
    prioridade: str,
    equipe_id: int,
    sugestao_categoria: str,
    sugestao_prioridade: str,
    sugestao_equipe_id: int,
    risco: bool,
    agora: datetime,
) -> int:
    conferencia_id = registrar_conferencia(
        conn,
        zona_id=zona_id,
        resultado="problema",
        usuario_id=usuario["id"],
        no_local=origem == "qr",
        agora=agora,
    )
    cursor = conn.execute(
        """
        INSERT INTO problemas (
          zona_id, conferencia_id, usuario_id, descricao, perto_de, origem,
          categoria, prioridade, equipe_id, sugestao_categoria, sugestao_prioridade,
          sugestao_equipe_id, confirmado, risco, status, criado_em
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, 'aberto', ?)
        """,
        (
            zona_id,
            conferencia_id,
            usuario["id"],
            descricao,
            perto_de or None,
            origem,
            categoria,
            prioridade,
            equipe_id,
            sugestao_categoria,
            sugestao_prioridade,
            sugestao_equipe_id,
            1 if risco else 0,
            iso(agora),
        ),
    )
    problema_id = int(cursor.lastrowid)
    onde = "pelo QR da zona" if origem == "qr" else "relatado à distância"
    perto = PERTO_DE_NOME.get(perto_de)
    detalhe = f" Perto de: {perto}." if perto else ""
    acrescentar_evento(
        conn,
        problema_id,
        "aberto",
        f"{usuario['nome']} ({usuario['funcao']}) registrou {onde}: {descricao}.{detalhe}",
        usuario["papel"],
        agora,
    )
    acrescentar_evento(
        conn,
        problema_id,
        "sugestao",
        (
            f"IA sugeriu {nome_categoria(sugestao_categoria)} · "
            f"{sugestao_prioridade}. Aguardando confirmação."
        ),
        "sistema",
        agora,
    )
    if risco:
        acrescentar_evento(
            conn,
            problema_id,
            "alerta_brigada",
            "Palavra de risco. Prioridade P1. Aviso: avise a brigada pelo rádio. "
            "O sistema não acionou ninguém.",
            "sistema",
            agora,
        )
    return problema_id


def _problema_status(conn: sqlite3.Connection, problema_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM problemas WHERE id = ?", (problema_id,)).fetchone()


def confirmar_problema(
    conn: sqlite3.Connection,
    *,
    problema_id: int,
    usuario: dict,
    categoria: str,
    prioridade: str,
    equipe_id: int,
    agora: datetime,
) -> bool:
    atual = _problema_status(conn, problema_id)
    if atual is None or atual["status"] == "resolvido":
        return False
    equipe_nome = conn.execute(
        "SELECT nome FROM equipes WHERE id = ?", (equipe_id,)
    ).fetchone()["nome"]
    conn.execute(
        """
        UPDATE problemas
        SET categoria = ?, prioridade = ?, equipe_id = ?, confirmado = 1
        WHERE id = ?
        """,
        (categoria, prioridade, equipe_id, problema_id),
    )
    acrescentar_evento(
        conn,
        problema_id,
        "confirmado",
        (
            f"{usuario['nome']} ({usuario['funcao']}) confirmou "
            f"{nome_categoria(categoria)} · {prioridade} · {equipe_nome}."
        ),
        usuario["papel"],
        agora,
    )
    return True


def assumir_problema(
    conn: sqlite3.Connection,
    *,
    problema_id: int,
    usuario: dict,
    agora: datetime,
) -> bool:
    atual = _problema_status(conn, problema_id)
    if atual is None or atual["status"] == "resolvido":
        return False
    if atual["status"] == "em_atendimento":
        return True
    conn.execute(
        "UPDATE problemas SET status = 'em_atendimento' WHERE id = ?",
        (problema_id,),
    )
    acrescentar_evento(
        conn,
        problema_id,
        "assumido",
        f"{usuario['nome']} ({usuario['funcao']}) assumiu o atendimento.",
        usuario["papel"],
        agora,
    )
    return True


def resolver_problema(
    conn: sqlite3.Connection,
    *,
    problema_id: int,
    usuario: dict,
    agora: datetime,
) -> bool:
    atual = _problema_status(conn, problema_id)
    if atual is None or atual["status"] == "resolvido":
        return False
    conn.execute(
        """
        UPDATE problemas
        SET status = 'resolvido', resolvido_em = ?
        WHERE id = ?
        """,
        (iso(agora), problema_id),
    )
    acrescentar_evento(
        conn,
        problema_id,
        "resolvido",
        f"{usuario['nome']} ({usuario['funcao']}) marcou como resolvido.",
        usuario["papel"],
        agora,
    )
    return True


def sugestao_equipe(conn: sqlite3.Connection, categoria: str) -> tuple[int, str]:
    return equipe_da_categoria(conn, categoria)
