"""Rotas da planta de fundo e do editor de blocos (só o gestor altera)."""

from __future__ import annotations

from flask import Blueprint, abort, render_template, request, send_file, url_for

from app.db import get_db
from app.planta import caminho_imagem, layout_de_todos, remover_imagem, salvar_imagem, salvar_layout
from app.rotas.acesso_web import so_gestor
from app.rotas.comum import corpo, json_resposta

bp = Blueprint("planta", __name__)


def _url_imagem(piso: str) -> str:
    return url_for("planta.imagem", piso=piso)


def _pisos_e_zonas() -> tuple[list[str], list[dict]]:
    zonas = [dict(r) for r in get_db().execute(
        "SELECT codigo, nome, piso, ordem_piso FROM zonas ORDER BY ordem_piso, nome")]
    pisos = list(dict.fromkeys(z["piso"] for z in zonas))
    return pisos, zonas


@bp.get("/mapa/layout")
def layout():
    return json_resposta({"pisos": layout_de_todos(get_db(), _url_imagem)})


@bp.get("/plantas/<piso>/imagem")
def imagem(piso: str):
    caminho = caminho_imagem(get_db(), piso)
    if caminho is None:
        abort(404)
    resposta = send_file(caminho, max_age=60)
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    return resposta


@bp.post("/plantas/<piso>/imagem")
@so_gestor
def enviar_imagem(piso: str):
    pisos, _ = _pisos_e_zonas()
    if piso not in pisos:
        return json_resposta({"erro": "piso_invalido"}, 400)
    arquivo = request.files.get("arquivo")
    if arquivo is None:
        return json_resposta({"erro": "arquivo_obrigatorio", "mensagem": "Escolha uma imagem."}, 400)
    db = get_db()
    try:
        with db:
            salvar_imagem(db, piso, arquivo.read())
    except ValueError as erro:
        return json_resposta({"erro": "imagem_invalida", "mensagem": str(erro)}, 400)
    return json_resposta({"pisos": layout_de_todos(db, _url_imagem)}, 201)


@bp.post("/plantas/<piso>/imagem/remover")
@so_gestor
def tirar_imagem(piso: str):
    db = get_db()
    with db:
        remover_imagem(db, piso)
    return json_resposta({"pisos": layout_de_todos(db, _url_imagem)})


@bp.post("/plantas/<piso>/layout")
@so_gestor
def gravar_layout(piso: str):
    pisos, zonas = _pisos_e_zonas()
    if piso not in pisos:
        return json_resposta({"erro": "piso_invalido"}, 400)
    validas = {z["codigo"] for z in zonas if z["piso"] == piso}
    db = get_db()
    try:
        with db:
            total = salvar_layout(db, piso, corpo(), validas)
    except (ValueError, TypeError, IndexError) as erro:
        return json_resposta({"erro": "layout_invalido", "mensagem": str(erro)}, 400)
    return json_resposta({"ok": True, "celulas": total, "pisos": layout_de_todos(db, _url_imagem)})


@bp.get("/telas/mapa/editar")
@so_gestor
def editor():
    pisos, zonas = _pisos_e_zonas()
    return render_template("editor_mapa.html", pagina="editor", pisos=pisos, zonas=zonas)
