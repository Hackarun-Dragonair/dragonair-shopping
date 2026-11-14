import pytest

from app import create_app
from app.modelo import limpar_cache


@pytest.fixture
def app(tmp_path):
    limpar_cache()
    aplicacao = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path / "teste.sqlite3"),
            "SEED_ON_START": True,
            "SECRET_KEY": "teste",
            "PLANTAS_DIR": str(tmp_path / "plantas"),
        }
    )
    yield aplicacao
    limpar_cache()


@pytest.fixture
def client(app):
    return app.test_client()
