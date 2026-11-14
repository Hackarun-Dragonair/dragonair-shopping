"""Tela de entrada (crachá fictício) e saída. A API JSON /entrar continua em painel.py."""

from __future__ import annotations

from functools import wraps

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.perfis import NOME_PERFIL, buscar_cracha, crachas_demo, perfil_do_papel, usuario_logado
from app.rotas.comum import json_resposta, quer_json

bp = Blueprint("acesso", __name__)


def _proximo_seguro(valor: str | None) -> str:
    # Só aceita caminho interno (evita redirecionar para outro site).
    if valor and valor.startswith("/") and not valor.startswith("//"):
        return valor
    return url_for("mapa.inicio")


def so_gestor(view):
    """Telas e ações do gestor. Sem login de gestor: tela pede o crachá (ou 403 na API)."""
    @wraps(view)
    def envolvida(*args, **kwargs):
        usuario = usuario_logado()
        if usuario and usuario["perfil"] == "gestor":
            return view(*args, **kwargs)
        if quer_json() or request.method != "GET":
            return json_resposta({"erro": "so_gestor", "mensagem": "Só o gestor pode fazer isso."}, 403)
        return redirect(url_for("acesso.entrar_tela", perfil="gestor", proximo=request.path))
    return envolvida


@bp.get("/entrar")
def entrar_tela():
    return render_template(
        "entrar.html",
        crachas=crachas_demo(),
        perfil=request.args.get("perfil", ""),
        proximo=_proximo_seguro(request.args.get("proximo")),
        erro=None,
    )


@bp.post("/entrar/cracha")
def entrar_cracha():
    codigo = (request.form.get("cracha") or "").strip()[:20]
    pedido = request.form.get("perfil", "")
    proximo = _proximo_seguro(request.form.get("proximo"))
    usuario, erro = buscar_cracha(codigo) if codigo else (None, "Digite o código do crachá.")
    if usuario and pedido in NOME_PERFIL and perfil_do_papel(usuario["papel"]) != pedido:
        erro = f"Este crachá é de {NOME_PERFIL[perfil_do_papel(usuario['papel'])]}, não de {NOME_PERFIL[pedido]}."
        usuario = None
    if usuario is None:
        return render_template(
            "entrar.html", crachas=crachas_demo(), perfil=pedido, proximo=proximo, erro=erro
        ), 400
    session.permanent = True  # o celular lembra o crachá
    session["usuario_codigo"] = usuario["codigo"]
    if perfil_do_papel(usuario["papel"]) == "gestor" and proximo == url_for("mapa.inicio"):
        proximo = url_for("telas.painel")
    return redirect(proximo)


@bp.post("/sair")
def sair():
    session.pop("usuario_codigo", None)
    return redirect(url_for("acesso.entrar_tela"))


@bp.app_context_processor
def _usuario_nas_telas():
    return {"usuario_atual": usuario_logado()}
