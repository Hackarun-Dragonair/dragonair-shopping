"""Sessão da demonstração e respostas JSON. Não há página aqui."""

from __future__ import annotations

from flask import jsonify, request, session

from app.db import get_db


def corpo() -> dict:
    dados = request.get_json(silent=True)
    if isinstance(dados, dict):
        return dados
    return request.form.to_dict(flat=True)


def json_resposta(payload, status: int = 200):
    resp = jsonify(payload)
    resp.headers["Cache-Control"] = "no-store"
    return resp, status


def ator_atual() -> dict:
    db = get_db()
    codigo = session.get("usuario_codigo") or request.headers.get("X-Usuario")
    row = None
    if codigo:
        row = db.execute(
            "SELECT * FROM usuarios WHERE codigo = ?", (codigo,)
        ).fetchone()
    if row is None:
        row = db.execute(
            """
            SELECT * FROM usuarios
            WHERE papel = 'encarregado'
            ORDER BY id LIMIT 1
            """
        ).fetchone()
    return dict(row)


def origem_do_pedido() -> str:
    origem = str(corpo().get("origem") or request.args.get("origem") or "qr")
    return origem if origem in {"qr", "lista"} else "qr"
