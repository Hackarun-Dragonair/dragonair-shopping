"""Telas (HTML) da fila, do problema, do painel e da IA.

Só leem dados com as mesmas funções do backend (app/consultas.py).
As ações (confirmar, assumir, resolver) são feitas pelo JavaScript chamando a API.
"""
from dataclasses import asdict

from flask import Blueprint, abort, render_template, request

from app.consultas import (
    agora_utc,
    indicadores,
    listar_equipes,
    listar_problemas,
    listar_zonas,
    montar_mapa,
    obter_problema,
)
from app.db import get_db
from app.dominio import CATEGORIAS, PRIORIDADES
from app.modelo import obter_modelo
from app.perfis import eh_gestor
from app.ritmo import listar_alertas

from app.rotas.acesso_web import so_gestor  # noqa: E402

bp = Blueprint("telas", __name__, url_prefix="/telas")


@bp.get("/fila")
def fila():
    """Quadro em 3 colunas: Aberto, Em atendimento e Resolvido (os últimos 8)."""
    filtros = {k: request.args.get(k, "") for k in ("prioridade", "equipe", "piso")}
    db = get_db()
    problemas = listar_problemas(db, status="todos", **filtros)
    colunas = {
        "aberto": [p for p in problemas if p["status"] == "aberto"],
        "em_atendimento": [p for p in problemas if p["status"] == "em_atendimento"],
        "resolvido": sorted(
            (p for p in problemas if p["status"] == "resolvido"),
            key=lambda p: p["resolvido_em"] or "", reverse=True,
        )[:8],
    }
    pisos = [r["piso"] for r in db.execute("SELECT DISTINCT piso, ordem_piso FROM zonas ORDER BY ordem_piso")]
    return render_template(
        "fila.html", pagina="fila", colunas=colunas, filtros=filtros,
        equipes=listar_equipes(db), pisos=pisos, prioridades=PRIORIDADES,
    )


@bp.get("/problemas/<int:problema_id>")
def problema(problema_id: int):
    item = obter_problema(get_db(), problema_id)
    if item is None:
        abort(404)
    return render_template(
        "problema.html", pagina="fila", p=item, pode_confirmar=eh_gestor(),
        equipes=listar_equipes(get_db()), categorias=CATEGORIAS, prioridades=PRIORIDADES,
    )


@bp.get("/painel")
@so_gestor
def painel():
    db = get_db()
    abertos = listar_problemas(db, status="abertos")
    por_equipe: dict[str, int] = {}
    for p in abertos:
        por_equipe[p["equipe_nome"]] = por_equipe.get(p["equipe_nome"], 0) + 1
    return render_template(
        "painel.html", pagina="painel", d=indicadores(db),
        zonas=montar_mapa(db)["zonas"], por_equipe=sorted(por_equipe.items(), key=lambda x: -x[1]),
        abertos=len(abertos), p1=sum(1 for p in abertos if p["prioridade"] == "P1"),
        alertas=listar_alertas(db, agora_utc()), ia=obter_modelo().relatorio,
    )


@bp.get("/sobre-a-ia")
def sobre_ia():
    modelo = obter_modelo()
    return render_template("sobre_ia.html", pagina="ia", fonte=modelo.fonte, r=asdict(modelo.relatorio))
