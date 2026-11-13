import sqlite3

import pytest


def test_linha_do_tempo_nao_apaga(app):
    with app.app_context():
        from app.db import get_db

        db = get_db()
        assert db.execute("SELECT COUNT(*) AS n FROM eventos").fetchone()["n"] > 0
        with pytest.raises(sqlite3.IntegrityError, match="nao pode ser apagada"):
            db.execute("DELETE FROM eventos")


def test_recriar_cenario_mantem_a_trava(app):
    with app.app_context():
        from app.db import get_db
        from app.seed import semear

        semear(get_db())
        db = get_db()
        assert db.execute("SELECT COUNT(*) AS n FROM eventos").fetchone()["n"] > 0
        with pytest.raises(sqlite3.IntegrityError, match="nao pode ser apagada"):
            db.execute("DELETE FROM eventos")


def test_linha_do_tempo_nao_altera(app):
    with app.app_context():
        from app.db import get_db

        db = get_db()
        with pytest.raises(sqlite3.IntegrityError, match="nao pode ser alterada"):
            db.execute("UPDATE eventos SET texto = 'apagado' WHERE id = (SELECT MIN(id) FROM eventos)")
