"""Câmera (só números) e sensor simulado abrindo ocorrência na mesma fila."""

from app.sensores import LEITURAS_SEGUIDAS


def _contar(client, zona, pessoas):
    return client.post("/eventos/camera", json={"zona": zona, "pessoas": pessoas})


def test_contagem_baixa_nao_abre_nada(client):
    resp = _contar(client, "praca-a", 2)
    assert resp.status_code == 200
    assert resp.get_json()["uso_alto"] is False


def test_uso_alto_precisa_de_leituras_seguidas(app, client):
    app.config["LIMITE_USO"] = 3
    for _ in range(LEITURAS_SEGUIDAS - 1):
        assert _contar(client, "praca-a", 5).get_json()["novo"] is False
    resp = _contar(client, "praca-a", 5)
    assert resp.status_code == 201
    dados = resp.get_json()
    assert dados["novo"] is True

    problema = client.get(f"/problemas/{dados['problema_id']}", headers={"Accept": "application/json"}).get_json()
    problema = problema.get("problema", problema)
    assert problema["categoria"] == "limpeza"
    assert problema["prioridade"] == "P3"
    assert problema["origem"] == "camera"
    assert problema["confirmado"] == 0  # a câmera sugere, a pessoa confirma
    assert "Nenhuma imagem" in problema["eventos"][0]["texto"]


def test_uma_leitura_baixa_no_meio_zera_a_sequencia(app, client):
    app.config["LIMITE_USO"] = 3
    _contar(client, "praca-a", 5)
    _contar(client, "praca-a", 5)
    _contar(client, "praca-a", 1)
    assert _contar(client, "praca-a", 5).get_json()["novo"] is False


def test_nao_duplica_enquanto_aberta(app, client):
    app.config["LIMITE_USO"] = 3
    ids = {_contar(client, "praca-a", 9).get_json()["problema_id"] for _ in range(LEITURAS_SEGUIDAS + 4)}
    ids.discard(None)
    assert len(ids) == 1


def test_contagem_aparece_no_mapa(client):
    _contar(client, "praca-b", 7)
    zonas = client.get("/mapa").get_json()["zonas"]
    praca = next(z for z in zonas if z["codigo"] == "praca-b")
    assert praca["pessoas"] == 7


def test_camera_nao_tira_zona_do_cinza(app, client):
    # praca-a começa sem conferência humana; contagem não conta como conferência.
    _contar(client, "praca-a", 1)
    zonas = client.get("/mapa").get_json()["zonas"]
    assert next(z for z in zonas if z["codigo"] == "praca-a")["estado"] == "cinza"


def test_entrada_invalida(client):
    assert _contar(client, "nao-existe", 3).status_code == 400
    assert _contar(client, "praca-a", -1).status_code == 400
    assert client.post("/eventos/camera", json={"zona": "praca-a"}).status_code == 400


def test_chave_da_camera(app, client):
    app.config["CAMERA_CHAVE"] = "segredo-de-teste"
    assert _contar(client, "praca-a", 3).status_code == 401
    resp = client.post(
        "/eventos/camera",
        json={"zona": "praca-a", "pessoas": 3},
        headers={"X-Chave-Camera": "segredo-de-teste"},
    )
    assert resp.status_code == 200


def test_sensor_fumaca_simulado_vira_p1_com_brigada(client):
    resp = client.post("/eventos/sensor", json={"zona": "doca-1", "tipo": "fumaca"})
    assert resp.status_code == 201
    pid = resp.get_json()["problema_id"]
    problema = client.get(f"/problemas/{pid}", headers={"Accept": "application/json"}).get_json()
    problema = problema.get("problema", problema)
    assert problema["prioridade"] == "P1"
    assert problema["risco"] == 1
    assert "SIMULADO" in problema["descricao"]
    assert any("brigada" in e["texto"] for e in problema["eventos"])

    de_novo = client.post("/eventos/sensor", json={"zona": "doca-1", "tipo": "fumaca"})
    assert de_novo.get_json()["problema_id"] == pid  # não duplica


def test_sensor_tipo_invalido(client):
    assert client.post("/eventos/sensor", json={"zona": "doca-1", "tipo": "x"}).status_code == 400
