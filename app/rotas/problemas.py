from flask import Blueprint, Response, abort, request

from app.dossie import texto_dossie
from app.consultas import (
    agora_utc,
    equipe_da_categoria,
    listar_equipes,
    listar_problemas,
    montar_mapa,
    obter_problema,
)
from app.db import get_db
from app.dominio import CATEGORIAS, PRIORIDADES
from app.rotas.comum import ator_atual, corpo, json_resposta
from app.servico import assumir_problema, confirmar_problema, resolver_problema

bp = Blueprint("problemas", __name__)


def _carregar(problema_id: int) -> dict:
    item = obter_problema(get_db(), problema_id)
    if item is None:
        abort(404)
    return item


@bp.get("/fila")
def fila():
    db = get_db()
    filtros = {
        "piso": request.args.get("piso", ""),
        "equipe": request.args.get("equipe", ""),
        "prioridade": request.args.get("prioridade", ""),
        "status": request.args.get("status", "abertos"),
    }
    mapa = montar_mapa(db)
    return json_resposta(
        {
            "problemas": listar_problemas(db, **filtros),
            "filtros": filtros,
            "pisos": [piso for piso, _zonas in mapa["pisos"]],
            "equipes": listar_equipes(db),
            "prioridades": list(PRIORIDADES),
        }
    )


@bp.get("/problemas/<int:problema_id>")
def detalhe(problema_id: int):
    return json_resposta(
        {
            "problema": _carregar(problema_id),
            "equipes": listar_equipes(get_db()),
            "categorias": [{"codigo": codigo, "nome": nome} for codigo, nome in CATEGORIAS],
            "prioridades": list(PRIORIDADES),
        }
    )


def _dados_confirmacao(problema: dict) -> tuple[str, str, int, str | None]:
    dados = corpo()
    categoria = str(dados.get("categoria") or problema["categoria"])
    if categoria not in {codigo for codigo, _nome in CATEGORIAS}:
        categoria = problema["categoria"]
    prioridade = str(dados.get("prioridade") or problema["prioridade"])
    aviso = None
    if problema["risco"]:
        if prioridade != "P1":
            aviso = "Prioridade mantida em P1. Palavra de risco não pode ser rebaixada."
        prioridade = "P1"
    elif prioridade not in PRIORIDADES:
        prioridade = problema["prioridade"]
    db = get_db()
    try:
        equipe_id = int(dados.get("equipe_id", problema["equipe_id"]))
    except (TypeError, ValueError):
        equipe_id = problema["equipe_id"]
    if db.execute("SELECT 1 FROM equipes WHERE id = ?", (equipe_id,)).fetchone() is None:
        equipe_id, _nome = equipe_da_categoria(db, categoria)
    return categoria, prioridade, equipe_id, aviso


@bp.get("/problemas/<int:problema_id>/dossie")
def dossie(problema_id: int):
    problema = _carregar(problema_id)
    texto = texto_dossie(problema)
    accept = request.headers.get("Accept", "")
    if "text/plain" in accept and "application/json" not in accept:
        return Response(texto, mimetype="text/plain; charset=utf-8")
    return json_resposta(
        {
            "problema_id": problema_id,
            "prioridade": problema["prioridade"],
            "status": problema["status"],
            "eventos": len(problema["eventos"]),
            "texto": texto,
        }
    )


@bp.post("/problemas/<int:problema_id>/confirmar")
def confirmar(problema_id: int):
    problema = _carregar(problema_id)
    categoria, prioridade, equipe_id, aviso = _dados_confirmacao(problema)
    db = get_db()
    with db:
        ok = confirmar_problema(
            db,
            problema_id=problema_id,
            usuario=ator_atual(),
            categoria=categoria,
            prioridade=prioridade,
            equipe_id=equipe_id,
            agora=agora_utc(),
        )
    return json_resposta(
        {"ok": ok, "aviso": aviso, "problema": obter_problema(db, problema_id)}
    )


@bp.post("/problemas/<int:problema_id>/assumir")
def assumir(problema_id: int):
    _carregar(problema_id)
    db = get_db()
    with db:
        ok = assumir_problema(
            db,
            problema_id=problema_id,
            usuario=ator_atual(),
            agora=agora_utc(),
        )
    return json_resposta({"ok": ok, "problema": obter_problema(db, problema_id)})


@bp.post("/problemas/<int:problema_id>/resolver")
def resolver(problema_id: int):
    _carregar(problema_id)
    db = get_db()
    with db:
        ok = resolver_problema(
            db,
            problema_id=problema_id,
            usuario=ator_atual(),
            agora=agora_utc(),
        )
    return json_resposta({"ok": ok, "problema": obter_problema(db, problema_id)})
