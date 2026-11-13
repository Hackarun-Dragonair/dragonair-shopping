"""Ocorrências abertas pelo sistema: câmera (contagem anônima) e sensor.

Regras combinadas com a banca:
- A câmera só manda NÚMEROS (pessoas na zona). Nenhuma imagem chega aqui.
- Movimento alto em várias leituras seguidas vira TAREFA DE LIMPEZA (P3),
  não "lotação". Limpeza por demanda, não por horário fixo.
- A câmera SUGERE. A ocorrência nasce sem confirmação e uma pessoa confirma.
  A zona só sai do cinza com conferência humana (QR).
- Sensor de fumaça usa a mesma regra de risco do QR: P1 + aviso à brigada.
  Na demo o sensor é SIMULADO e isso aparece no texto da ocorrência.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta

from app.consultas import equipe_da_categoria, iso, parse_iso
from app.servico import acrescentar_evento

# Pessoas na zona, por tipo de zona, a partir das quais o uso é "alto".
# Números fictícios para a demo; cada shopping ajusta os seus.
LIMITE_USO_POR_TIPO = {
    "praca_alimentacao": 25,
    "sanitario": 8,  # câmera no CORREDOR dos banheiros, nunca dentro
    "corredor": 30,
}
LIMITE_USO_PADRAO = 20

LEITURAS_SEGUIDAS = 3  # histerese: precisa ficar alto em 3 leituras seguidas
ESPERA_MINUTOS = 30  # depois de abrir, não abre outra na mesma zona por 30 min

SENSORES = {"fumaca": "Sensor de fumaça"}


def limite_uso(zona: dict, limite_fixo: int | None = None) -> int:
    """Limite da zona. `limite_fixo` vem da config (demo com webcam usa 3)."""
    if limite_fixo:
        return int(limite_fixo)
    return LIMITE_USO_POR_TIPO.get(zona["tipo"], LIMITE_USO_PADRAO)


def gravar_leitura(
    conn: sqlite3.Connection, zona_id: int, fonte: str, tipo: str, valor: int, agora: datetime
) -> None:
    conn.execute(
        "INSERT INTO leituras (zona_id, fonte, tipo, valor, criado_em) VALUES (?, ?, ?, ?, ?)",
        (zona_id, fonte, tipo, valor, iso(agora)),
    )


def _ultimas_contagens(conn: sqlite3.Connection, zona_id: int, quantas: int) -> list[int]:
    rows = conn.execute(
        """
        SELECT valor FROM leituras
        WHERE zona_id = ? AND fonte = 'camera' AND tipo = 'pessoas'
        ORDER BY id DESC LIMIT ?
        """,
        (zona_id, quantas),
    ).fetchall()
    return [row["valor"] for row in rows]


def _ocorrencia_recente(
    conn: sqlite3.Connection, zona_id: int, origem: str, agora: datetime
) -> sqlite3.Row | None:
    """Aberta, ou criada há menos de ESPERA_MINUTOS (evita duplicar)."""
    row = conn.execute(
        """
        SELECT * FROM problemas
        WHERE zona_id = ? AND origem = ?
        ORDER BY id DESC LIMIT 1
        """,
        (zona_id, origem),
    ).fetchone()
    if row is None:
        return None
    if row["status"] != "resolvido":
        return row
    criada = parse_iso(row["criado_em"])
    if criada and agora - criada < timedelta(minutes=ESPERA_MINUTOS):
        return row
    return None


def _inserir_ocorrencia(
    conn: sqlite3.Connection,
    *,
    zona_id: int,
    descricao: str,
    origem: str,
    categoria: str,
    prioridade: str,
    risco: bool,
    agora: datetime,
) -> int:
    equipe_id, _nome = equipe_da_categoria(conn, categoria)
    cursor = conn.execute(
        """
        INSERT INTO problemas (
          zona_id, conferencia_id, usuario_id, descricao, perto_de, origem,
          categoria, prioridade, equipe_id, sugestao_categoria, sugestao_prioridade,
          sugestao_equipe_id, confirmado, risco, status, criado_em
        ) VALUES (?, NULL, NULL, ?, NULL, ?, ?, ?, ?, ?, ?, ?, 0, ?, 'aberto', ?)
        """,
        (
            zona_id, descricao, origem, categoria, prioridade, equipe_id,
            categoria, prioridade, equipe_id, 1 if risco else 0, iso(agora),
        ),
    )
    return int(cursor.lastrowid)


def processar_contagem(
    conn: sqlite3.Connection,
    *,
    zona: dict,
    pessoas: int,
    agora: datetime,
    limite_fixo: int | None = None,
) -> dict:
    """Grava a contagem e, se o uso ficou alto, abre a tarefa de limpeza."""
    gravar_leitura(conn, zona["id"], "camera", "pessoas", pessoas, agora)
    limite = limite_uso(zona, limite_fixo)
    ultimas = _ultimas_contagens(conn, zona["id"], LEITURAS_SEGUIDAS)
    uso_alto = len(ultimas) == LEITURAS_SEGUIDAS and all(v >= limite for v in ultimas)
    resposta = {"zona": zona["codigo"], "pessoas": pessoas, "limite": limite,
                "uso_alto": uso_alto, "problema_id": None, "novo": False}
    if not uso_alto:
        return resposta
    existente = _ocorrencia_recente(conn, zona["id"], "camera", agora)
    if existente is not None:
        resposta["problema_id"] = existente["id"]
        return resposta
    media = round(sum(ultimas) / len(ultimas))
    problema_id = _inserir_ocorrencia(
        conn,
        zona_id=zona["id"],
        descricao=f"Movimento alto (média de {media} pessoas). Reforçar limpeza e recolher bandejas.",
        origem="camera",
        categoria="limpeza",
        prioridade="P3",
        risco=False,
        agora=agora,
    )
    acrescentar_evento(
        conn, problema_id, "aberto",
        (f"Câmera (contagem anônima) viu {media} pessoas em {LEITURAS_SEGUIDAS} leituras "
         f"seguidas, acima do limite de {limite}. Nenhuma imagem foi guardada."),
        "sistema", agora,
    )
    acrescentar_evento(
        conn, problema_id, "sugestao",
        "Sistema sugeriu Limpeza · P3. Aguardando confirmação de uma pessoa.",
        "sistema", agora,
    )
    resposta.update(problema_id=problema_id, novo=True)
    return resposta


def processar_sensor(
    conn: sqlite3.Connection, *, zona: dict, tipo: str, simulado: bool, agora: datetime
) -> dict:
    """Sensor de fumaça: P1, risco e aviso à brigada. Não rebaixa."""
    nome = SENSORES[tipo] + (" (SIMULADO)" if simulado else "")
    gravar_leitura(conn, zona["id"], "sensor", tipo, 1, agora)
    existente = conn.execute(
        """
        SELECT id FROM problemas
        WHERE zona_id = ? AND origem = 'sensor' AND status != 'resolvido'
        ORDER BY id DESC LIMIT 1
        """,
        (zona["id"],),
    ).fetchone()
    if existente is not None:
        acrescentar_evento(conn, existente["id"], "sensor", f"{nome} disparou de novo.", "sistema", agora)
        return {"zona": zona["codigo"], "problema_id": existente["id"], "novo": False}
    problema_id = _inserir_ocorrencia(
        conn,
        zona_id=zona["id"],
        descricao=f"{nome} disparou: possível fumaça.",
        origem="sensor",
        categoria="seguranca",
        prioridade="P1",
        risco=True,
        agora=agora,
    )
    acrescentar_evento(conn, problema_id, "aberto", f"{nome} disparou na zona.", "sistema", agora)
    acrescentar_evento(
        conn, problema_id, "alerta_brigada",
        "Palavra de risco. Prioridade P1. Aviso: avise a brigada pelo rádio. "
        "O sistema não acionou ninguém.",
        "sistema", agora,
    )
    return {"zona": zona["codigo"], "problema_id": problema_id, "novo": True}


def pessoas_agora(conn: sqlite3.Connection, agora: datetime, validade_segundos: int = 60) -> dict[int, int]:
    """Última contagem de cada zona, se for recente. Zona sem câmera não aparece."""
    resultado: dict[int, int] = {}
    for row in conn.execute(
        """
        SELECT l.zona_id, l.valor, l.criado_em FROM leituras l
        JOIN (SELECT zona_id, MAX(id) AS id FROM leituras
              WHERE fonte = 'camera' AND tipo = 'pessoas' GROUP BY zona_id) u
          ON u.id = l.id
        """
    ):
        momento = parse_iso(row["criado_em"])
        if momento and (agora - momento).total_seconds() <= validade_segundos:
            resultado[row["zona_id"]] = row["valor"]
    return resultado
