"""Entradas automáticas: câmera (só números) e sensor. Ver app/sensores.py."""

from __future__ import annotations

from flask import Blueprint, current_app, request

from app.consultas import agora_utc, obter_zona
from app.db import get_db
from app.rotas.comum import corpo, json_resposta
from app.sensores import SENSORES, pessoas_agora, processar_contagem, processar_sensor

bp = Blueprint("eventos", __name__, url_prefix="/eventos")


def _chave_ok() -> bool:
    """Se CAMERA_CHAVE estiver configurada, o script precisa mandar a mesma."""
    esperada = current_app.config.get("CAMERA_CHAVE")
    return not esperada or request.headers.get("X-Chave-Camera") == esperada


def _zona(dados: dict):
    return obter_zona(get_db(), str(dados.get("zona", "")))


@bp.post("/camera")
def camera():
    if not _chave_ok():
        return json_resposta({"erro": "chave_invalida"}, 401)
    dados = corpo()
    zona = _zona(dados)
    if zona is None:
        return json_resposta({"erro": "zona_invalida"}, 400)
    try:
        pessoas = int(dados.get("pessoas"))
    except (TypeError, ValueError):
        return json_resposta({"erro": "pessoas_invalido"}, 400)
    if pessoas < 0 or pessoas > 1000:
        return json_resposta({"erro": "pessoas_invalido"}, 400)
    db = get_db()
    with db:
        resposta = processar_contagem(
            db, zona=zona, pessoas=pessoas, agora=agora_utc(),
            limite_fixo=current_app.config.get("LIMITE_USO"),
        )
    return json_resposta(resposta, 201 if resposta["novo"] else 200)


@bp.post("/sensor")
def sensor():
    if not _chave_ok():
        return json_resposta({"erro": "chave_invalida"}, 401)
    dados = corpo()
    zona = _zona(dados)
    if zona is None:
        return json_resposta({"erro": "zona_invalida"}, 400)
    tipo = str(dados.get("tipo", ""))
    if tipo not in SENSORES:
        return json_resposta({"erro": "tipo_invalido"}, 400)
    # Até existir sensor de verdade, tudo é SIMULADO (regulamento 6.5).
    simulado = str(dados.get("simulado", "1")) not in {"0", "false", "False"}
    db = get_db()
    with db:
        resposta = processar_sensor(db, zona=zona, tipo=tipo, simulado=simulado, agora=agora_utc())
    if not request.is_json and request.form:
        from flask import redirect, url_for
        return redirect(url_for("telas.problema", problema_id=resposta["problema_id"]))
    return json_resposta(resposta, 201 if resposta["novo"] else 200)


@bp.get("/movimento")
def movimento():
    db = get_db()
    contagens = pessoas_agora(db, agora_utc())
    zonas = db.execute("SELECT id, codigo, nome FROM zonas ORDER BY ordem_piso, nome").fetchall()
    return json_resposta({
        "zonas": [
            {"codigo": z["codigo"], "nome": z["nome"], "pessoas": contagens[z["id"]]}
            for z in zonas if z["id"] in contagens
        ]
    })
