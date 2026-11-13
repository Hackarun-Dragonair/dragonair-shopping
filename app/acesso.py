"""Celular autorizado e crachá. Troca o usuário fictício da demo."""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime

from app.consultas import iso


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def autorizar_dispositivo(
    conn: sqlite3.Connection,
    *,
    apelido: str,
    token: str,
    agora: datetime,
) -> dict:
    resumo = hash_token(token)
    existe = conn.execute(
        "SELECT id, apelido FROM dispositivos WHERE token_hash = ?",
        (resumo,),
    ).fetchone()
    if existe is not None:
        return {"id": existe["id"], "apelido": existe["apelido"], "novo": False}
    cursor = conn.execute(
        """
        INSERT INTO dispositivos (token_hash, apelido, autorizado_em)
        VALUES (?, ?, ?)
        """,
        (resumo, apelido, iso(agora)),
    )
    return {"id": int(cursor.lastrowid), "apelido": apelido, "novo": True}


def entrar_com_cracha(
    conn: sqlite3.Connection, *, codigo: str, token: str
) -> tuple[dict | None, str | None]:
    """Devolve o usuário e, se recusar, o código do erro."""
    aparelho = conn.execute(
        "SELECT id FROM dispositivos WHERE token_hash = ?",
        (hash_token(token),),
    ).fetchone()
    if aparelho is None:
        return None, "aparelho_nao_autorizado"
    cracha = conn.execute(
        """
        SELECT c.ativo, u.*
        FROM crachas c
        JOIN usuarios u ON u.id = c.usuario_id
        WHERE c.codigo = ?
        """,
        (codigo.strip().upper(),),
    ).fetchone()
    if cracha is None:
        return None, "cracha_desconhecido"
    if not cracha["ativo"]:
        return None, "cracha_inativo"
    return dict(cracha), None
