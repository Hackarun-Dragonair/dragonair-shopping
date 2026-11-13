"""Reaplica o que o celular guardou enquanto estava sem rede."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from app.consultas import equipe_da_categoria, iso, obter_zona
from app.dominio import CATEGORIAS, triar
from app.modelo import obter_modelo
from app.servico import abrir_problema, registrar_conferencia


def _marcar(conn: sqlite3.Connection, chave: str, tipo: str, agora: datetime) -> bool:
    try:
        conn.execute(
            "INSERT INTO envios (chave, tipo, criado_em) VALUES (?, ?, ?)",
            (chave, tipo, iso(agora)),
        )
    except sqlite3.IntegrityError:
        return False
    return True


def _aplicar_um(
    conn: sqlite3.Connection,
    item: dict,
    usuario: dict,
    agora: datetime,
) -> dict:
    chave = str(item.get("chave") or "").strip()
    tipo = str(item.get("tipo") or "")
    if not chave:
        return {"chave": "", "status": "erro", "erro": "chave_obrigatoria"}
    if tipo not in {"conferencia", "problema"}:
        return {"chave": chave, "status": "erro", "erro": "tipo_invalido"}
    zona = obter_zona(conn, str(item.get("zona") or ""))
    if zona is None:
        return {"chave": chave, "status": "erro", "erro": "zona_desconhecida"}
    if tipo == "conferencia" and str(item.get("resultado") or "") not in {"ok", "atencao"}:
        return {"chave": chave, "status": "erro", "erro": "resultado_invalido"}
    if tipo == "problema" and not str(item.get("descricao") or "").strip():
        return {"chave": chave, "status": "erro", "erro": "descricao_obrigatoria"}
    if not _marcar(conn, chave, tipo, agora):
        return {"chave": chave, "status": "ignorado"}

    if tipo == "conferencia":
        resultado = str(item.get("resultado") or "")
        registrar_conferencia(
            conn,
            zona_id=zona["id"],
            resultado=resultado,
            usuario_id=usuario["id"],
            no_local=True,
            agora=agora,
        )
        return {"chave": chave, "status": "aplicado", "resultado": resultado}

    descricao = str(item.get("descricao") or "").strip()[:500]
    sugestao = triar(descricao, obter_modelo().prever(descricao))
    categoria = str(item.get("categoria") or sugestao.categoria)
    if categoria not in {codigo for codigo, _nome in CATEGORIAS}:
        categoria = sugestao.categoria
    equipe_id, _nome = equipe_da_categoria(conn, categoria)
    problema_id = abrir_problema(
        conn,
        zona_id=zona["id"],
        usuario=usuario,
        descricao=descricao,
        perto_de="",
        origem="qr",
        categoria=categoria,
        prioridade=sugestao.prioridade,
        equipe_id=equipe_id,
        sugestao_categoria=sugestao.categoria,
        sugestao_prioridade=sugestao.prioridade,
        sugestao_equipe_id=equipe_id,
        risco=sugestao.risco,
        agora=agora,
    )
    return {
        "chave": chave,
        "status": "aplicado",
        "problema_id": problema_id,
        "prioridade": sugestao.prioridade,
        "risco": sugestao.risco,
    }


def aplicar_fila(
    conn: sqlite3.Connection,
    itens: list,
    usuario: dict,
    agora: datetime,
) -> list[dict]:
    saida = []
    for item in itens:
        if not isinstance(item, dict):
            saida.append({"chave": "", "status": "erro", "erro": "item_invalido"})
            continue
        with conn:
            saida.append(_aplicar_um(conn, item, usuario, agora))
    return saida
