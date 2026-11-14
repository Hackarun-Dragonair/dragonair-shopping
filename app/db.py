"""SQLite da demonstração. A linha do tempo só aceita INSERT."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS equipes (
  id INTEGER PRIMARY KEY,
  codigo TEXT NOT NULL UNIQUE,
  nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
  id INTEGER PRIMARY KEY,
  codigo TEXT NOT NULL UNIQUE,
  nome TEXT NOT NULL,
  papel TEXT NOT NULL CHECK (papel IN ('encarregado','supervisor','coordenacao','manutencao')),
  funcao TEXT NOT NULL,
  equipe_id INTEGER REFERENCES equipes(id)
);

CREATE TABLE IF NOT EXISTS zonas (
  id INTEGER PRIMARY KEY,
  codigo TEXT NOT NULL UNIQUE,
  nome TEXT NOT NULL,
  tipo TEXT NOT NULL,
  piso TEXT NOT NULL,
  ordem_piso INTEGER NOT NULL,
  prazo_minutos INTEGER NOT NULL,
  local_qr TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encaminhamento (
  categoria TEXT PRIMARY KEY,
  equipe_id INTEGER NOT NULL REFERENCES equipes(id)
);

CREATE TABLE IF NOT EXISTS conferencias (
  id INTEGER PRIMARY KEY,
  zona_id INTEGER NOT NULL REFERENCES zonas(id),
  resultado TEXT NOT NULL CHECK (resultado IN ('ok','atencao','problema')),
  usuario_id INTEGER REFERENCES usuarios(id),
  no_local INTEGER NOT NULL CHECK (no_local IN (0, 1)),
  criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS problemas (
  id INTEGER PRIMARY KEY,
  zona_id INTEGER NOT NULL REFERENCES zonas(id),
  conferencia_id INTEGER REFERENCES conferencias(id),
  usuario_id INTEGER REFERENCES usuarios(id),
  descricao TEXT NOT NULL,
  perto_de TEXT,
  origem TEXT NOT NULL CHECK (origem IN ('qr','lista')),
  categoria TEXT NOT NULL,
  prioridade TEXT NOT NULL CHECK (prioridade IN ('P1','P2','P3','P4')),
  equipe_id INTEGER NOT NULL REFERENCES equipes(id),
  sugestao_categoria TEXT NOT NULL,
  sugestao_prioridade TEXT NOT NULL,
  sugestao_equipe_id INTEGER REFERENCES equipes(id),
  confirmado INTEGER NOT NULL DEFAULT 0 CHECK (confirmado IN (0, 1)),
  risco INTEGER NOT NULL DEFAULT 0 CHECK (risco IN (0, 1)),
  status TEXT NOT NULL CHECK (status IN ('aberto','em_atendimento','resolvido')),
  criado_em TEXT NOT NULL,
  resolvido_em TEXT
);

CREATE TABLE IF NOT EXISTS eventos (
  id INTEGER PRIMARY KEY,
  problema_id INTEGER NOT NULL REFERENCES problemas(id),
  tipo TEXT NOT NULL,
  texto TEXT NOT NULL,
  papel TEXT NOT NULL,
  criado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dispositivos (
  id INTEGER PRIMARY KEY,
  token_hash TEXT NOT NULL UNIQUE,
  apelido TEXT NOT NULL,
  autorizado_em TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crachas (
  id INTEGER PRIMARY KEY,
  codigo TEXT NOT NULL UNIQUE,
  usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
  ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS envios (
  id INTEGER PRIMARY KEY,
  chave TEXT NOT NULL UNIQUE,
  tipo TEXT NOT NULL,
  criado_em TEXT NOT NULL
);

-- Planta de fundo e blocos do mapa (desenhados pelo gestor). Ficam fora do seed.
CREATE TABLE IF NOT EXISTS plantas (
  piso TEXT PRIMARY KEY,
  arquivo TEXT,
  proporcao REAL NOT NULL DEFAULT 0.62,
  colunas INTEGER NOT NULL DEFAULT 40,
  linhas INTEGER NOT NULL DEFAULT 25
);

CREATE TABLE IF NOT EXISTS celulas (
  piso TEXT NOT NULL,
  col INTEGER NOT NULL,
  lin INTEGER NOT NULL,
  zona_codigo TEXT NOT NULL,
  PRIMARY KEY (piso, col, lin)
);

CREATE INDEX IF NOT EXISTS idx_conferencias_zona ON conferencias (zona_id, criado_em);
CREATE INDEX IF NOT EXISTS idx_problemas_zona ON problemas (zona_id, status);
CREATE INDEX IF NOT EXISTS idx_eventos_problema ON eventos (problema_id, id);
"""


def caminho_banco() -> Path:
    return Path(current_app.config["DATABASE"])


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        destino = caminho_banco()
        destino.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(destino)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def fechar_db(_exc=None) -> None:
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def instalar_triggers(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TRIGGER IF EXISTS eventos_sem_update")
    conn.execute("DROP TRIGGER IF EXISTS eventos_sem_delete")
    conn.execute(
        """
        CREATE TRIGGER eventos_sem_update
        BEFORE UPDATE ON eventos
        BEGIN
          SELECT RAISE(ABORT, 'linha do tempo nao pode ser alterada');
        END
        """
    )
    conn.execute(
        """
        CREATE TRIGGER eventos_sem_delete
        BEFORE DELETE ON eventos
        BEGIN
          SELECT RAISE(ABORT, 'linha do tempo nao pode ser apagada');
        END
        """
    )


def init_db() -> None:
    db = get_db()
    db.executescript(SCHEMA)
    instalar_triggers(db)
    db.commit()


def banco_vazio() -> bool:
    total = get_db().execute("SELECT COUNT(*) AS n FROM zonas").fetchone()["n"]
    return total == 0
