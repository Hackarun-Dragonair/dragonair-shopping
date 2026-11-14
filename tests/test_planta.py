"""Planta de fundo + bloquinhos do mapa (editor do gestor)."""
import io

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64  # cabeçalho de PNG basta para o teste


def _gestor(client):
    client.post("/entrar/cracha", data={"cracha": "OTTO", "perfil": "gestor"})


def test_funcionario_nao_edita(client):
    client.post("/entrar/cracha", data={"cracha": "RITA", "perfil": "funcionario"})
    assert client.get("/telas/mapa/editar").status_code == 302
    assert client.post("/plantas/L1/layout", json={"celulas": []}).status_code == 403


def test_gestor_envia_planta_e_pinta_blocos(client):
    _gestor(client)
    assert client.get("/telas/mapa/editar").status_code == 200
    resp = client.post("/plantas/L1/imagem", data={"arquivo": (io.BytesIO(PNG), "planta.png")},
                       content_type="multipart/form-data")
    assert resp.status_code == 201
    assert resp.get_json()["pisos"]["L1"]["imagem"]
    assert client.get("/plantas/L1/imagem").status_code == 200
    resp = client.post("/plantas/L1/layout", json={
        "colunas": 20, "linhas": 10, "proporcao": 0.5,
        "celulas": [[0, 0, "praca-a"], [1, 0, "praca-a"], [5, 5, "sanitario-piso1"]]})
    assert resp.status_code == 200 and resp.get_json()["celulas"] == 3
    lay = client.get("/mapa/layout").get_json()["pisos"]["L1"]
    assert [0, 0, "praca-a"] in lay["celulas"] and lay["colunas"] == 20


def test_rejeita_arquivo_que_nao_e_imagem(client):
    _gestor(client)
    resp = client.post("/plantas/L1/imagem", data={"arquivo": (io.BytesIO(b"<script>"), "x.png")},
                       content_type="multipart/form-data")
    assert resp.status_code == 400


def test_recusa_envio_grande_demais(client):
    _gestor(client)
    grande = PNG + b"\x00" * (10 * 1024 * 1024)  # 10 MB, acima do limite de 9 MB
    resp = client.post("/plantas/L1/imagem", data={"arquivo": (io.BytesIO(grande), "planta.png")},
                       content_type="multipart/form-data")
    assert resp.status_code == 413


def test_rejeita_zona_de_outro_piso_e_grade_invalida(client):
    _gestor(client)
    assert client.post("/plantas/L1/layout", json={"celulas": [[0, 0, "doca-1"]]}).status_code == 400
    assert client.post("/plantas/L1/layout", json={"colunas": 500, "linhas": 10}).status_code == 400
    assert client.post("/plantas/NaoExiste/layout", json={}).status_code == 400
