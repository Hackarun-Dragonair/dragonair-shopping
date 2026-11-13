"""Prazo sugerido pelo histórico e alertas por zona.

O prazo gravado na zona não muda. A sugestão é só uma leitura,
para o mapa cinza continuar usando o prazo combinado.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta

from app.consultas import iso, parse_iso

# Natal e véspera de Ano-Novo: o prédio enche e o prazo sugerido cai pela metade.
EVENTOS_DO_PREDIO = ((12, 24), (12, 25), (12, 31))


def _mediana(valores: list[float]) -> float:
    ordem = sorted(valores)
    meio = len(ordem) // 2
    if len(ordem) % 2:
        return ordem[meio]
    return (ordem[meio - 1] + ordem[meio]) / 2


def prazo_sugerido(conn: sqlite3.Connection, zona: dict, agora: datetime) -> dict:
    atual = int(zona["prazo_minutos"])
    if (agora.month, agora.day) in EVENTOS_DO_PREDIO:
        return {
            "codigo": zona["codigo"],
            "prazo_minutos": atual,
            "prazo_sugerido": max(15, atual // 2),
            "amostras": 0,
            "motivo": "evento",
        }
    momentos = [
        parse_iso(row["criado_em"])
        for row in conn.execute(
            """
            SELECT criado_em FROM conferencias
            WHERE zona_id = ?
            ORDER BY id
            """,
            (zona["id"],),
        )
    ]
    intervalos = []
    for anterior, seguinte in zip(momentos, momentos[1:]):
        if anterior and seguinte:
            intervalos.append((seguinte - anterior).total_seconds() / 60)
    if len(intervalos) < 2:
        sugerido, motivo = atual, "sem_historico"
    else:
        sugerido = int(round(_mediana(intervalos)))
        sugerido = min(240, max(15, sugerido))
        motivo = "ritmo"
    return {
        "codigo": zona["codigo"],
        "prazo_minutos": atual,
        "prazo_sugerido": sugerido,
        "amostras": len(intervalos),
        "motivo": motivo,
    }


def listar_alertas(conn: sqlite3.Connection, agora: datetime) -> dict:
    limite = iso(agora)
    corte = iso(agora - timedelta(days=7))
    divergentes = [
        {"codigo": row["codigo"], "nome": row["nome"], "tipo": "ok_divergente"}
        for row in conn.execute(
            """
            SELECT z.codigo, z.nome
            FROM zonas z
            JOIN conferencias c ON c.id = (
              SELECT MAX(id) FROM conferencias WHERE zona_id = z.id
            )
            WHERE c.resultado = 'ok'
              AND EXISTS (
                SELECT 1 FROM problemas p
                WHERE p.zona_id = z.id AND p.status != 'resolvido'
              )
            ORDER BY z.nome
            """
        )
    ]
    sem_achados = [
        {"codigo": row["codigo"], "nome": row["nome"], "tipo": "semana_sem_achados"}
        for row in conn.execute(
            """
            SELECT z.codigo, z.nome
            FROM zonas z
            WHERE EXISTS (
              SELECT 1 FROM conferencias c
              WHERE c.zona_id = z.id AND c.criado_em >= ?
            )
              AND NOT EXISTS (
                SELECT 1 FROM problemas p
                WHERE p.zona_id = z.id AND p.criado_em >= ?
              )
              AND (
                SELECT resultado FROM conferencias
                WHERE zona_id = z.id
                ORDER BY id DESC
                LIMIT 1
              ) = 'ok'
            ORDER BY z.nome
            """,
            (corte, corte),
        )
    ]
    return {
        "gerado_em": limite,
        "ok_divergente": divergentes,
        "semana_sem_achados": sem_achados,
    }
