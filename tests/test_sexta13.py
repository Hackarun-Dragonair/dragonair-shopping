"""Easter Egg: gato preto na zona esquecida há mais tempo (sexta-feira 13)."""

from datetime import datetime, timezone

from app.sexta13 import ativo, eh_sexta_13, zona_do_gato


def _zonas(client):
    return client.get("/mapa").get_json()["zonas"]


def test_data_sexta_13():
    assert eh_sexta_13(datetime(2026, 11, 13, 15, tzinfo=timezone.utc))
    assert not eh_sexta_13(datetime(2026, 11, 14, 15, tzinfo=timezone.utc))
    # 13/11 às 01h UTC ainda é dia 12 em Palmas (UTC-3)
    assert not eh_sexta_13(datetime(2026, 11, 13, 1, tzinfo=timezone.utc))


def test_modos():
    sabado = datetime(2026, 11, 14, 15, tzinfo=timezone.utc)
    assert ativo(sabado, "1")
    assert not ativo(sabado, "auto")
    assert not ativo(datetime(2026, 11, 13, 15, tzinfo=timezone.utc), "0")


def test_gato_vai_na_zona_nunca_conferida():
    zonas = [
        {"codigo": "a", "estado": "cinza", "ultima_em": "2026-11-13T10:00:00+00:00"},
        {"codigo": "b", "estado": "cinza", "ultima_em": ""},
        {"codigo": "c", "estado": "ok", "ultima_em": ""},
    ]
    assert zona_do_gato(zonas) == "b"


def test_sem_zona_cinza_sem_gato():
    assert zona_do_gato([{"codigo": "a", "estado": "ok", "ultima_em": ""}]) is None


def test_desligado_nao_tem_gato(app, client):
    app.config["SEXTA13"] = "0"
    assert not any(z["gato"] for z in _zonas(client))
    assert "🐈‍⬛" not in client.get("/").get_data(as_text=True)


def test_um_gato_so_e_frase_uma_vez(app, client):
    app.config["SEXTA13"] = "1"
    com_gato = [z for z in _zonas(client) if z["gato"]]
    assert len(com_gato) == 1
    assert com_gato[0]["estado"] == "cinza"
    pagina = client.get("/").get_data(as_text=True)
    assert pagina.count("Sexta-feira 13: um gato preto") == 1


def test_conferir_espanta_e_gato_pula(app, client):
    app.config["SEXTA13"] = "1"
    primeira = next(z for z in _zonas(client) if z["gato"])["codigo"]
    resp = client.post(f"/z/{primeira}/conferir", json={"resultado": "ok"})
    assert resp.get_json()["espantou_gato"] is True
    nova = [z for z in _zonas(client) if z["gato"]]
    assert all(z["codigo"] != primeira for z in nova)  # pulou para outra esquecida


def test_tela_mostra_gato_espantado(app, client):
    app.config["SEXTA13"] = "1"
    zona = next(z for z in _zonas(client) if z["gato"])["codigo"]
    resp = client.post(f"/z/{zona}/conferir", data={"resultado": "ok", "origem": "qr"})
    assert "espantou=1" in resp.headers["Location"]
    assert "Gato preto espantado" in client.get(resp.headers["Location"]).get_data(as_text=True)
