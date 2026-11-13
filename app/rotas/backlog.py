"""Rotas do backlog de backend. Só JSON e o PDF das etiquetas."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, Response

from app.acesso import autorizar_dispositivo, entrar_com_cracha
from app.consultas import agora_utc, listar_zonas, obter_zona
from app.db import get_db
from app.etiquetas import pdf_etiquetas
from app.fila_envio import aplicar_fila
from app.ritmo import listar_alertas, prazo_sugerido
from app.rotas.comum import ator_atual, corpo, json_resposta
from app.rotas.mapa import url_da_zona

bp = Blueprint("backlog", __name__)


def _etiquetas() -> list[dict]:
    return [
        {
            "codigo": zona["codigo"],
            "nome": zona["nome"],
            "piso": zona["piso"],
            "local_qr": zona["local_qr"],
            "url": url_da_zona(zona["codigo"]),
        }
        for zona in listar_zonas(get_db())
    ]


@bp.post("/dispositivos")
def dispositivos():
    dados = corpo()
    apelido = str(dados.get("apelido") or "").strip()[:80]
    token = str(dados.get("token") or "").strip()
    if len(apelido) < 2 or len(token) < 8:
        return json_resposta({"erro": "dados_invalidos"}, 400)
    db = get_db()
    with db:
        aparelho = autorizar_dispositivo(
            db, apelido=apelido, token=token, agora=agora_utc()
        )
    return json_resposta({"aparelho": aparelho}, 201 if aparelho["novo"] else 200)


@bp.post("/crachas/entrar")
def cracha():
    dados = corpo()
    codigo = str(dados.get("codigo") or "")
    token = str(dados.get("token") or "")
    if not codigo or not token:
        return json_resposta({"erro": "dados_invalidos"}, 400)
    usuario, erro = entrar_com_cracha(get_db(), codigo=codigo, token=token)
    if erro == "aparelho_nao_autorizado":
        return json_resposta({"erro": erro}, 403)
    if erro == "cracha_desconhecido":
        return json_resposta({"erro": erro}, 404)
    if erro:
        return json_resposta({"erro": erro}, 403)
    from flask import session

    session["usuario_codigo"] = usuario["codigo"]
    return json_resposta(
        {
            "usuario": {
                "codigo": usuario["codigo"],
                "nome": usuario["nome"],
                "papel": usuario["papel"],
            }
        }
    )


@bp.post("/fila-envio")
def fila_envio():
    itens = corpo().get("itens")
    if not isinstance(itens, list) or not itens:
        return json_resposta({"erro": "itens_obrigatorios"}, 400)
    db = get_db()
    resultado = aplicar_fila(db, itens, ator_atual(), agora_utc())
    return json_resposta({"itens": resultado})


@bp.get("/alertas")
def alertas():
    return json_resposta(listar_alertas(get_db(), agora_utc()))


@bp.get("/zonas/<codigo>/ritmo")
def ritmo(codigo: str):
    zona = obter_zona(get_db(), codigo)
    if zona is None:
        from flask import abort

        abort(404)
    quando = _agora_do_pedido()
    return json_resposta(prazo_sugerido(get_db(), zona, quando))


def _agora_do_pedido() -> datetime:
    from flask import request

    bruto = request.args.get("agora", "")
    if bruto:
        # O "+" do fuso vira espaço na query string.
        if " " in bruto:
            bruto = bruto.replace(" ", "+", 1)
        try:
            momento = datetime.fromisoformat(bruto)
        except ValueError:
            return agora_utc()
        if momento.tzinfo is None:
            momento = momento.replace(tzinfo=timezone.utc)
        return momento
    return agora_utc()


@bp.get("/etiquetas")
def etiquetas():
    return json_resposta({"etiquetas": _etiquetas()})


@bp.get("/etiquetas.pdf")
def etiquetas_pdf():
    arquivo = pdf_etiquetas(_etiquetas())
    resposta = Response(arquivo, mimetype="application/pdf")
    resposta.headers["Content-Disposition"] = "attachment; filename=etiquetas.pdf"
    return resposta
