from flask import Blueprint, current_app, render_template, request, url_for

from app.consultas import indicadores, listar_problemas, listar_zonas, montar_mapa
from app.db import get_db
from app.modelo import obter_modelo
from app.sexta13 import FRASE as FRASE_SEXTA13
from app.rotas.comum import json_resposta, quer_json

bp = Blueprint("mapa", __name__)


def url_da_zona(codigo: str) -> str:
    caminho = url_for("zona.ver", codigo=codigo)
    base = current_app.config.get("PUBLIC_BASE_URL", "").rstrip("/")
    if base:
        return base + caminho
    return request.host_url.rstrip("/") + caminho


def _com_url(mapa: dict) -> dict:
    for zona in mapa["zonas"]:
        zona["url"] = url_da_zona(zona["codigo"])
    for _piso, zonas in mapa["pisos"]:
        for zona in zonas:
            zona["url"] = url_da_zona(zona["codigo"])
    return mapa


@bp.get("/")
def inicio():
    if quer_json():
        return json_resposta(
            {
                "servico": "ronda-viva",
                "endpoints": {
                    "saude": "/saude",
                    "mapa": "/mapa",
                    "fila": "/fila",
                    "painel": "/painel",
                    "modelo": "/sobre-o-modelo",
                    "usuarios": "/usuarios",
                    "zona": "/z/<codigo>",
                    "dossie": "/problemas/<id>/dossie",
                    "dispositivos": "/dispositivos",
                    "cracha": "/crachas/entrar",
                    "fila_envio": "/fila-envio",
                    "alertas": "/alertas",
                    "ritmo": "/zonas/<codigo>/ritmo",
                    "etiquetas": "/etiquetas",
                },
            }
        )
    db = get_db()
    return render_template(
        "inicio.html", pagina="mapa", zonas=listar_zonas(db), frase_sexta13=FRASE_SEXTA13,
        d=indicadores(db), abertos=listar_problemas(db, status="abertos"), ia=obter_modelo().relatorio,
    )


@bp.get("/mapa")
def mapa():
    return json_resposta(_com_url(montar_mapa(get_db())))
