"""Banco SQLite do Ronda Viva.

Dono: BACKEND (tarefa #2).
O banco é apagado e recriado toda vez que o servidor liga, com as zonas de dados/zonas.csv.
As tabelas seguem docs/contrato.md (seção 3).
"""
import csv
import sqlite3
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_BANCO = RAIZ / "ronda.db"
ARQUIVO_ZONAS = RAIZ / "dados" / "zonas.csv"

ESQUEMA = """
CREATE TABLE zonas (
    id TEXT PRIMARY KEY, nome TEXT NOT NULL, tipo TEXT NOT NULL, piso INTEGER NOT NULL,
    x INTEGER, y INTEGER, largura INTEGER, altura INTEGER, prazo_min INTEGER NOT NULL
);
CREATE TABLE registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT, zona_id TEXT NOT NULL REFERENCES zonas(id),
    status TEXT NOT NULL, texto TEXT, criado_em TEXT NOT NULL
);
CREATE TABLE ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT, registro_id INTEGER REFERENCES registros(id),
    zona_id TEXT NOT NULL REFERENCES zonas(id), texto TEXT,
    categoria TEXT, prioridade TEXT, equipe TEXT,
    estado TEXT NOT NULL DEFAULT 'aberto', risco INTEGER NOT NULL DEFAULT 0, criado_em TEXT NOT NULL
);
CREATE TABLE eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ocorrencia_id INTEGER NOT NULL REFERENCES ocorrencias(id),
    tipo TEXT NOT NULL, detalhe TEXT, criado_em TEXT NOT NULL
);
-- Linha do tempo é só de inserir: o próprio banco recusa alterar ou apagar.
CREATE TRIGGER eventos_sem_update BEFORE UPDATE ON eventos
BEGIN SELECT RAISE(ABORT, 'eventos nao podem ser alterados'); END;
CREATE TRIGGER eventos_sem_delete BEFORE DELETE ON eventos
BEGIN SELECT RAISE(ABORT, 'eventos nao podem ser apagados'); END;
"""


def agora_iso() -> str:
    """Data e hora atual no formato do contrato (ex.: 2026-11-13T19:30:00)."""
    return datetime.now().isoformat(timespec="seconds")


def conectar() -> sqlite3.Connection:
    """Abre o banco. As linhas vêm como dicionário (linha["nome"])."""
    con = sqlite3.connect(ARQUIVO_BANCO)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def recriar() -> None:
    """Apaga o banco, cria as tabelas e carrega as zonas do CSV."""
    ARQUIVO_BANCO.unlink(missing_ok=True)
    with conectar() as con:
        con.executescript(ESQUEMA)
        with open(ARQUIVO_ZONAS, encoding="utf-8") as f:
            for z in csv.DictReader(f):
                con.execute(
                    "INSERT INTO zonas VALUES (:id, :nome, :tipo, :piso, :x, :y, :largura, :altura, :prazo_min)",
                    z,
                )
