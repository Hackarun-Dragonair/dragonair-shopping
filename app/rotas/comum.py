"""Sessão da demonstração e respostas JSON. Não há página aqui."""

from __future__ import annotations

from flask import current_app, jsonify, request, session

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
    """Quem está agindo: o crachá da sessão; sem crachá, o aparelho de campo."""
    db = get_db()
    codigo = session.get("usuario_codigo")
    if not codigo and current_app.config.get("TESTING"):
        codigo = request.headers.get("X-Usuario")  # atalho só para testes
    row = None
    if codigo:
        row = db.execute("SELECT * FROM usuarios WHERE codigo = ?", (codigo,)).fetchone()
    if row is None:
        row = db.execute("SELECT * FROM usuarios WHERE codigo = 'campo'").fetchone()
    if row is None:
        row = db.execute(
            "SELECT * FROM usuarios WHERE papel = 'encarregado' ORDER BY id LIMIT 1"
        ).fetchone()
    return dict(row)


def quer_json() -> bool:
    if request.args.get("format") == "json":
        return True
    if request.is_json:
        return True
    accept = request.accept_mimetypes
    return accept["application/json"] > accept["text/html"] and accept["application/json"] > 0


def origem_do_pedido() -> str:
    origem = str(corpo().get("origem") or request.args.get("origem") or "qr")
    return origem if origem in {"qr", "lista"} else "qr"
