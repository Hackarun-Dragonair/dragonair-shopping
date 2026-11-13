"""Telas (HTML) da fila, do problema, do painel e da IA.

Só leem dados com as mesmas funções do backend (app/consultas.py).
As ações (confirmar, assumir, resolver) são feitas pelo JavaScript chamando a API.
"""
from dataclasses import asdict

from flask import Blueprint, abort, render_template, request

from app.consultas import indicadores, listar_equipes, listar_problemas, obter_problema
from app.db import get_db
from app.dominio import CATEGORIAS, PRIORIDADES
from app.modelo import obter_modelo

bp = Blueprint("telas", __name__, url_prefix="/telas")


@bp.get("/fila")
def fila():
    status = request.args.get("status", "abertos")
    problemas = listar_problemas(get_db(), status=status)
    return render_template("fila.html", pagina="fila", problemas=problemas, status=status)


@bp.get("/problemas/<int:problema_id>")
def problema(problema_id: int):
    item = obter_problema(get_db(), problema_id)
    if item is None:
        abort(404)
    return render_template(
        "problema.html", pagina="fila", p=item,
        equipes=listar_equipes(get_db()), categorias=CATEGORIAS, prioridades=PRIORIDADES,
    )


@bp.get("/painel")
def painel():
    return render_template("painel.html", pagina="painel", d=indicadores(get_db()))


@bp.get("/sobre-a-ia")
def sobre_ia():
    modelo = obter_modelo()
    return render_template("sobre_ia.html", pagina="ia", fonte=modelo.fonte, r=asdict(modelo.relatorio))
