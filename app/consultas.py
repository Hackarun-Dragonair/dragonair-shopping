"""Leituras do mapa, da fila e do painel."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

from app.dominio import estado_da_zona, ha_quanto, nome_categoria

SP = timezone(timedelta(hours=-3))
ORDEM_ESTADO = {"problema": 0, "cinza": 1, "atencao": 2, "ok": 3}
ROTULO_STATUS = {
    "aberto": "Aberto",
    "em_atendimento": "Em atendimento",
    "resolvido": "Resolvido",
}


def agora_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(momento: datetime) -> str:
    return momento.replace(microsecond=0).isoformat()


def parse_iso(valor: str | None) -> datetime | None:
    if not valor:
        return None
    return datetime.fromisoformat(valor)


def formato_local(valor: str | None) -> str:
    momento = parse_iso(valor)
    if momento is None:
        return ""
    return momento.astimezone(SP).strftime("%d/%m %H:%M")


def listar_usuarios(conn: sqlite3.Connection) -> list[dict]:
    return [dict(row) for row in conn.execute("SELECT * FROM usuarios ORDER BY id")]


def listar_equipes(conn: sqlite3.Connection) -> list[dict]:
    return [dict(row) for row in conn.execute("SELECT * FROM equipes ORDER BY nome")]


def equipe_da_categoria(conn: sqlite3.Connection, categoria: str) -> tuple[int, str]:
    row = conn.execute(
        """
        SELECT e.id, e.nome
        FROM encaminhamento c
        JOIN equipes e ON e.id = c.equipe_id
        WHERE c.categoria = ?
        """,
        (categoria,),
    ).fetchone()
    if row is None:
        row = conn.execute(
            "SELECT id, nome FROM equipes WHERE codigo = 'manutencao'"
        ).fetchone()
    return row["id"], row["nome"]


def _reincidencias(conn: sqlite3.Connection, agora: datetime) -> dict[int, list[str]]:
    limite = iso(agora - timedelta(days=7))
    linhas = conn.execute(
        """
        SELECT zona_id, categoria, COUNT(*) AS n
        FROM problemas
        WHERE criado_em >= ?
        GROUP BY zona_id, categoria
        HAVING n >= 2
        """,
        (limite,),
    ).fetchall()
    por_zona: dict[int, list[str]] = {}
    for linha in linhas:
        por_zona.setdefault(linha["zona_id"], []).append(
            f"{nome_categoria(linha['categoria'])} ×{linha['n']}"
        )
    return por_zona


def listar_zonas(conn: sqlite3.Connection, agora: datetime | None = None) -> list[dict]:
    agora = agora or agora_utc()
    abertos = {
        row["zona_id"]: row["id"]
        for row in conn.execute(
            """
            SELECT zona_id, id FROM problemas
            WHERE status != 'resolvido'
            ORDER BY id
            """
        )
    }
    ultimas = {
        row["zona_id"]: row
        for row in conn.execute(
            """
            SELECT c.zona_id, c.resultado, c.criado_em, c.no_local
            FROM conferencias c
            JOIN (
              SELECT zona_id, MAX(id) AS id
              FROM conferencias
              GROUP BY zona_id
            ) ultima ON ultima.id = c.id
            """
        )
    }
    repetidas = _reincidencias(conn, agora)
    zonas = []
    for row in conn.execute("SELECT * FROM zonas ORDER BY ordem_piso, nome"):
        ultima = ultimas.get(row["id"])
        momento = parse_iso(ultima["criado_em"]) if ultima else None
        estado = estado_da_zona(
            ultimo_resultado=ultima["resultado"] if ultima else None,
            ultima_em=momento,
            prazo_minutos=row["prazo_minutos"],
            problema_aberto=row["id"] in abertos,
            agora=agora,
        )
        item = dict(row)
        item.update(
            {
                "estado": estado,
                "rotulo": {
                    "ok": "OK",
                    "atencao": "Atenção",
                    "problema": "Problema",
                    "cinza": "Sem conferência",
                }[estado],
                "ha": ha_quanto(momento, agora),
                "quando": formato_local(ultima["criado_em"]) if ultima else "",
                "problema_id": abertos.get(row["id"]),
                "reincidencia": repetidas.get(row["id"], []),
            }
        )
        zonas.append(item)
    return zonas


def obter_zona(conn: sqlite3.Connection, codigo: str, agora: datetime | None = None) -> dict | None:
    for zona in listar_zonas(conn, agora):
        if zona["codigo"] == codigo:
            return zona
    return None


def historico_zona(conn: sqlite3.Connection, zona_id: int) -> list[dict]:
    rotulos = {"ok": "OK", "atencao": "Atenção", "problema": "Problema"}
    linhas = []
    for row in conn.execute(
        """
        SELECT resultado, no_local, criado_em
        FROM conferencias
        WHERE zona_id = ?
        ORDER BY id DESC
        LIMIT 8
        """,
        (zona_id,),
    ):
        linhas.append(
            {
                "resultado": rotulos[row["resultado"]],
                "origem": "no QR" if row["no_local"] else "à distância",
                "quando": formato_local(row["criado_em"]),
            }
        )
    return linhas


def montar_mapa(conn: sqlite3.Connection, agora: datetime | None = None) -> dict:
    zonas = listar_zonas(conn, agora)
    piores = sorted(zonas, key=lambda zona: (ORDEM_ESTADO[zona["estado"]], zona["nome"]))
    pisos: list[tuple[str, list[dict]]] = []
    for zona in zonas:
        if not pisos or pisos[-1][0] != zona["piso"]:
            pisos.append((zona["piso"], []))
        pisos[-1][1].append(zona)
    cinza = sum(1 for zona in zonas if zona["estado"] == "cinza")
    return {
        "zonas": piores,
        "pisos": pisos,
        "cinza": cinza,
        "total": len(zonas),
    }


def listar_problemas(
    conn: sqlite3.Connection,
    *,
    piso: str = "",
    equipe: str = "",
    prioridade: str = "",
    status: str = "abertos",
) -> list[dict]:
    filtros = ["1 = 1"]
    params: list[str] = []
    if piso:
        filtros.append("z.piso = ?")
        params.append(piso)
    if equipe:
        filtros.append("e.codigo = ?")
        params.append(equipe)
    if prioridade:
        filtros.append("p.prioridade = ?")
        params.append(prioridade)
    if status != "todos":
        filtros.append("p.status != 'resolvido'")
    rows = conn.execute(
        f"""
        SELECT p.*, z.nome AS zona_nome, z.codigo AS zona_codigo, z.piso,
               e.nome AS equipe_nome, e.codigo AS equipe_codigo
        FROM problemas p
        JOIN zonas z ON z.id = p.zona_id
        JOIN equipes e ON e.id = p.equipe_id
        WHERE {' AND '.join(filtros)}
        ORDER BY p.prioridade, p.id DESC
        """,
        params,
    ).fetchall()
    itens = []
    for row in rows:
        item = dict(row)
        item["categoria_nome"] = nome_categoria(row["categoria"])
        item["status_nome"] = ROTULO_STATUS[row["status"]]
        item["quando"] = formato_local(row["criado_em"])
        item["sugestao_nome"] = nome_categoria(row["sugestao_categoria"])
        itens.append(item)
    return itens


def obter_problema(conn: sqlite3.Connection, problema_id: int) -> dict | None:
    row = conn.execute(
        """
        SELECT p.*, z.nome AS zona_nome, z.codigo AS zona_codigo, z.piso,
               z.local_qr, e.nome AS equipe_nome
        FROM problemas p
        JOIN zonas z ON z.id = p.zona_id
        JOIN equipes e ON e.id = p.equipe_id
        WHERE p.id = ?
        """,
        (problema_id,),
    ).fetchone()
    if row is None:
        return None
    item = dict(row)
    item["categoria_nome"] = nome_categoria(row["categoria"])
    item["status_nome"] = ROTULO_STATUS[row["status"]]
    item["quando"] = formato_local(row["criado_em"])
    item["resolvido_quando"] = formato_local(row["resolvido_em"])
    item["sugestao_nome"] = nome_categoria(row["sugestao_categoria"])
    item["eventos"] = [
        {
            "texto": evento["texto"],
            "papel": evento["papel"],
            "quando": formato_local(evento["criado_em"]),
        }
        for evento in conn.execute(
            "SELECT * FROM eventos WHERE problema_id = ? ORDER BY id",
            (problema_id,),
        )
    ]
    return item


def indicadores(conn: sqlite3.Connection, agora: datetime | None = None) -> dict:
    agora = agora or agora_utc()
    mapa = montar_mapa(conn, agora)
    total = mapa["total"] or 1
    no_prazo = mapa["total"] - mapa["cinza"]
    tempos = []
    for row in conn.execute(
        """
        SELECT criado_em, resolvido_em FROM problemas
        WHERE status = 'resolvido' AND resolvido_em IS NOT NULL
        """
    ):
        inicio = parse_iso(row["criado_em"])
        fim = parse_iso(row["resolvido_em"])
        if inicio and fim:
            tempos.append((fim - inicio).total_seconds() / 60)
    media = round(sum(tempos) / len(tempos)) if tempos else None
    repetidas = [
        zona["nome"]
        for zona in mapa["zonas"]
        if zona["reincidencia"]
    ]
    return {
        "zonas_no_prazo_pct": round(100 * no_prazo / total),
        "zonas_no_prazo": no_prazo,
        "total_zonas": mapa["total"],
        "zonas_cinza": mapa["cinza"],
        "tempo_medio_min": media,
        "problemas_resolvidos": len(tempos),
        "reincidencia": len(repetidas),
        "zonas_reincidentes": repetidas,
    }
