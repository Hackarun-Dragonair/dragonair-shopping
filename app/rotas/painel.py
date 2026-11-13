from dataclasses import asdict

from flask import Blueprint, session

from app.consultas import indicadores, listar_usuarios
from app.db import get_db
from app.modelo import obter_modelo
from app.rotas.comum import corpo, json_resposta

bp = Blueprint("painel", __name__)


@bp.get("/painel")
def painel():
    return json_resposta(indicadores(get_db()))


@bp.get("/sobre-o-modelo")
def sobre():
    modelo = obter_modelo()
    return json_resposta({"fonte": modelo.fonte, "relatorio": asdict(modelo.relatorio)})


@bp.get("/usuarios")
def usuarios():
    return json_resposta({"usuarios": listar_usuarios(get_db())})


@bp.post("/entrar")
def entrar():
    """API: entrar com crachá fictício. `usuario_codigo` direto só vale nos testes."""
    dados = corpo()
    from flask import current_app
    from app.perfis import buscar_cracha

    if dados.get("cracha"):
        usuario, erro = buscar_cracha(str(dados["cracha"]))
        if usuario is None:
            return json_resposta({"erro": "cracha_invalido", "mensagem": erro}, 404)
        codigo = usuario["codigo"]
    elif current_app.config.get("TESTING"):
        codigo = str(dados.get("usuario_codigo", ""))
    else:
        return json_resposta({"erro": "cracha_obrigatorio"}, 400)
    row = get_db().execute(
        "SELECT * FROM usuarios WHERE codigo = ?", (codigo,)
    ).fetchone()
    if row is None:
        return json_resposta({"erro": "usuario_desconhecido"}, 404)
    session["usuario_codigo"] = row["codigo"]
    return json_resposta({"usuario": dict(row)})
