"""Testa se as telas abrem. Dono: BACKEND."""
from fastapi.testclient import TestClient

from app.main import app


def test_telas_abrem():
    with TestClient(app) as cliente:
        for rota in ["/", "/z/sanitario-fem-p1", "/fila", "/painel", "/sobre-modelo", "/api/zonas"]:
            assert cliente.get(rota).status_code == 200, rota


def test_salvar_conferencia():
    with TestClient(app) as cliente:
        r = cliente.post("/z/sanitario-fem-p1", data={"status": "ok"}, follow_redirects=False)
        assert r.status_code == 303
        zona = next(z for z in cliente.get("/api/zonas").json() if z["id"] == "sanitario-fem-p1")
        assert zona["cor"] == "verde"


def test_zona_inexistente():
    with TestClient(app) as cliente:
        assert cliente.get("/z/nao-existe").status_code == 404
