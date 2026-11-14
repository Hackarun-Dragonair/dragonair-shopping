"""Planta de fundo e blocos do mapa.

O gestor envia a imagem da planta de um piso e marca, numa grade de
bloquinhos por cima dela, quais bloquinhos formam cada setor (zona).
A imagem fica só no servidor (pasta instance/, fora do Git): a planta
real nunca entra no repositório. Sem imagem, o mapa usa o desenho
fictício da equipe.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app

TIPOS = {b"\x89PNG": ".png", b"\xff\xd8\xff": ".jpg", b"RIFF": ".webp"}
TAMANHO_MAX = 8 * 1024 * 1024  # 8 MB
GRADE_MIN, GRADE_MAX = 10, 80


def pasta_plantas() -> Path:
    pasta = Path(current_app.config.get("PLANTAS_DIR") or Path(current_app.instance_path) / "plantas")
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def nome_seguro(piso: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in piso.lower())[:40] or "piso"


def extensao_da_imagem(conteudo: bytes) -> str | None:
    """Confere o tipo pelo começo do arquivo (não confia no nome)."""
    for assinatura, ext in TIPOS.items():
        if conteudo.startswith(assinatura):
            if ext == ".webp" and conteudo[8:12] != b"WEBP":
                return None
            return ext
    return None


def _garantir(conn: sqlite3.Connection, piso: str) -> None:
    conn.execute("INSERT OR IGNORE INTO plantas (piso) VALUES (?)", (piso,))


def salvar_imagem(conn: sqlite3.Connection, piso: str, conteudo: bytes) -> str:
    ext = extensao_da_imagem(conteudo)
    if ext is None:
        raise ValueError("Envie uma imagem PNG, JPG ou WEBP.")
    if len(conteudo) > TAMANHO_MAX:
        raise ValueError("Imagem maior que 8 MB.")
    pasta = pasta_plantas()
    base = nome_seguro(piso)
    for antigo in pasta.glob(base + ".*"):
        antigo.unlink()
    arquivo = base + ext
    (pasta / arquivo).write_bytes(conteudo)
    _garantir(conn, piso)
    conn.execute("UPDATE plantas SET arquivo = ? WHERE piso = ?", (arquivo, piso))
    return arquivo


def remover_imagem(conn: sqlite3.Connection, piso: str) -> None:
    row = conn.execute("SELECT arquivo FROM plantas WHERE piso = ?", (piso,)).fetchone()
    if row and row["arquivo"]:
        caminho = pasta_plantas() / row["arquivo"]
        if caminho.exists():
            caminho.unlink()
    conn.execute("UPDATE plantas SET arquivo = NULL WHERE piso = ?", (piso,))


def caminho_imagem(conn: sqlite3.Connection, piso: str) -> Path | None:
    row = conn.execute("SELECT arquivo FROM plantas WHERE piso = ?", (piso,)).fetchone()
    if not row or not row["arquivo"]:
        return None
    caminho = pasta_plantas() / row["arquivo"]
    return caminho if caminho.exists() else None


def salvar_layout(conn: sqlite3.Connection, piso: str, dados: dict, zonas_validas: set[str]) -> int:
    """Troca a grade e os bloquinhos do piso. Devolve quantos bloquinhos ficaram."""
    colunas = int(dados.get("colunas", 40))
    linhas = int(dados.get("linhas", 25))
    proporcao = float(dados.get("proporcao", 0.62))
    if not (GRADE_MIN <= colunas <= GRADE_MAX and GRADE_MIN <= linhas <= GRADE_MAX):
        raise ValueError(f"A grade deve ter de {GRADE_MIN} a {GRADE_MAX} colunas e linhas.")
    if not 0.2 <= proporcao <= 3:
        raise ValueError("Proporção da imagem inválida.")
    celulas = []
    for item in dados.get("celulas", []):
        col, lin, codigo = int(item[0]), int(item[1]), str(item[2])
        if not (0 <= col < colunas and 0 <= lin < linhas):
            continue
        if codigo not in zonas_validas:
            raise ValueError(f"Zona desconhecida: {codigo}")
        celulas.append((piso, col, lin, codigo))
    _garantir(conn, piso)
    conn.execute(
        "UPDATE plantas SET colunas = ?, linhas = ?, proporcao = ? WHERE piso = ?",
        (colunas, linhas, proporcao, piso),
    )
    conn.execute("DELETE FROM celulas WHERE piso = ?", (piso,))
    conn.executemany(
        "INSERT OR REPLACE INTO celulas (piso, col, lin, zona_codigo) VALUES (?, ?, ?, ?)", celulas
    )
    return len(celulas)


def layout_de_todos(conn: sqlite3.Connection, url_imagem) -> dict:
    """Layout de cada piso que o gestor configurou (para o mapa e o editor)."""
    pisos: dict[str, dict] = {}
    for row in conn.execute("SELECT * FROM plantas"):
        tem_imagem = bool(row["arquivo"]) and (pasta_plantas() / row["arquivo"]).exists()
        pisos[row["piso"]] = {
            "imagem": url_imagem(row["piso"]) if tem_imagem else None,
            "proporcao": row["proporcao"],
            "colunas": row["colunas"],
            "linhas": row["linhas"],
            "celulas": [],
        }
    for row in conn.execute("SELECT * FROM celulas ORDER BY piso, lin, col"):
        if row["piso"] in pisos:
            pisos[row["piso"]]["celulas"].append([row["col"], row["lin"], row["zona_codigo"]])
    return pisos
