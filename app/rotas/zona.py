from dataclasses import asdict

from flask import Blueprint, abort, request

from app.consultas import agora_utc, equipe_da_categoria, historico_zona, listar_equipes, obter_zona
from app.db import get_db
from app.dominio import (
    AVISO_BRIGADA,
    BOTOES_POR_TIPO,
    CATEGORIAS,
    PERTO_DE,
    garantir_prioridade,
    triar,
)
from app.modelo import obter_modelo
from app.rotas.comum import ator_atual, corpo, json_resposta, origem_do_pedido
from app.servico import abrir_problema, registrar_conferencia

bp = Blueprint("zona", __name__)


def _zona_ou_404(codigo: str) -> dict:
    zona = obter_zona(get_db(), codigo)
    if zona is None:
        abort(404)
    return zona


def _descricao() -> str:
    dados = corpo()
    texto = str(dados.get("pronto") or dados.get("descricao") or "")
    return texto.strip()[:500]


def _perto() -> str:
    perto = str(corpo().get("perto_de") or "")
    if perto not in {codigo for codigo, _nome in PERTO_DE}:
        return ""
    return perto


@bp.get("/z/<codigo>")
def ver(codigo: str):
    zona = _zona_ou_404(codigo)
    return json_resposta(
        {
            "zona": zona,
            "historico": historico_zona(get_db(), zona["id"]),
            "origem": origem_do_pedido(),
            "botoes": list(BOTOES_POR_TIPO.get(zona["tipo"], ())),
            "perto_de": [{"codigo": codigo_perto, "nome": nome} for codigo_perto, nome in PERTO_DE],
        }
    )


@bp.post("/z/<codigo>/conferir")
def conferir(codigo: str):
    zona = _zona_ou_404(codigo)
    resultado = str(corpo().get("resultado", ""))
    origem = origem_do_pedido()
    if resultado == "problema":
        return json_resposta(
            {"acao": "abrir_problema", "codigo": codigo, "origem": origem}
        )
    if resultado not in {"ok", "atencao"}:
        return json_resposta({"erro": "resultado_invalido"}, 400)
    db = get_db()
    with db:
        registrar_conferencia(
            db,
            zona_id=zona["id"],
            resultado=resultado,
            usuario_id=ator_atual()["id"],
            no_local=origem == "qr",
            agora=agora_utc(),
        )
    return json_resposta(
        {"resultado": resultado, "zona": _zona_ou_404(codigo)},
        201,
    )


@bp.get("/z/<codigo>/problema")
def formulario(codigo: str):
    zona = _zona_ou_404(codigo)
    return json_resposta(
        {
            "zona": zona,
            "origem": origem_do_pedido(),
            "botoes": list(BOTOES_POR_TIPO.get(zona["tipo"], ())),
            "perto_de": [{"codigo": codigo_perto, "nome": nome} for codigo_perto, nome in PERTO_DE],
            "categorias": [{"codigo": codigo_cat, "nome": nome} for codigo_cat, nome in CATEGORIAS],
        }
    )


@bp.post("/z/<codigo>/triagem")
def triagem(codigo: str):
    zona = _zona_ou_404(codigo)
    descricao = _descricao()
    if not descricao:
        return json_resposta({"erro": "descricao_obrigatoria"}, 400)
    sugestao = triar(descricao, obter_modelo().prever(descricao))
    db = get_db()
    equipe_id, equipe_nome = equipe_da_categoria(db, sugestao.categoria)
    alternativa = None
    if sugestao.alternativa:
        alt_id, alt_nome = equipe_da_categoria(db, sugestao.alternativa)
        alternativa = {"equipe_id": alt_id, "equipe_nome": alt_nome}
    return json_resposta(
        {
            "zona": {"codigo": zona["codigo"], "nome": zona["nome"]},
            "descricao": descricao,
            "perto_de": _perto(),
            "origem": origem_do_pedido(),
            "sugestao": asdict(sugestao),
            "equipe_id": equipe_id,
            "equipe_nome": equipe_nome,
            "alternativa_equipe": alternativa,
            "equipes": listar_equipes(db),
            "categorias": [{"codigo": codigo_cat, "nome": nome} for codigo_cat, nome in CATEGORIAS],
        }
    )


@bp.post("/z/<codigo>/problema")
def criar(codigo: str):
    zona = _zona_ou_404(codigo)
    descricao = _descricao()
    if not descricao:
        return json_resposta({"erro": "descricao_obrigatoria"}, 400)
    dados = corpo()
    categoria = str(dados.get("categoria", ""))
    if categoria not in {codigo_cat for codigo_cat, _nome in CATEGORIAS}:
        return json_resposta({"erro": "categoria_invalida"}, 400)
    origem = origem_do_pedido()
    perto = _perto()
    sugestao = triar(descricao, obter_modelo().prever(descricao))
    db = get_db()
    aviso = None
    editado = str(dados.get("editado", "")) == "1"
    if editado:
        pedida = str(dados.get("prioridade", "P4"))
        prioridade, risco = garantir_prioridade(descricao, pedida)
        if risco and pedida != "P1":
            aviso = "Prioridade mantida em P1. Palavra de risco não pode ser rebaixada."
        try:
            equipe_id = int(dados.get("equipe_id", ""))
        except (TypeError, ValueError):
            equipe_id = 0
        if db.execute("SELECT 1 FROM equipes WHERE id = ?", (equipe_id,)).fetchone() is None:
            equipe_id, _nome = equipe_da_categoria(db, categoria)
    else:
        prioridade = sugestao.prioridade
        risco = sugestao.risco
        equipe_id, _nome = equipe_da_categoria(db, categoria)
    if risco and aviso is None:
        aviso = AVISO_BRIGADA

    sugestao_categoria = str(dados.get("sugestao_categoria") or sugestao.categoria)
    sugestao_prioridade = str(dados.get("sugestao_prioridade") or sugestao.prioridade)
    try:
        sugestao_equipe_id = int(dados.get("sugestao_equipe_id", ""))
    except (TypeError, ValueError):
        sugestao_equipe_id, _nome = equipe_da_categoria(db, sugestao_categoria)

    with db:
        problema_id = abrir_problema(
            db,
            zona_id=zona["id"],
            usuario=ator_atual(),
            descricao=descricao,
            perto_de=perto,
            origem=origem,
            categoria=categoria,
            prioridade=prioridade,
            equipe_id=equipe_id,
            sugestao_categoria=sugestao_categoria,
            sugestao_prioridade=sugestao_prioridade,
            sugestao_equipe_id=sugestao_equipe_id,
            risco=risco,
            agora=agora_utc(),
        )
    from app.consultas import obter_problema

    return json_resposta(
        {"problema": obter_problema(db, problema_id), "aviso": aviso},
        201,
    )
