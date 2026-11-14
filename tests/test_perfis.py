"""Login por crachá fictício: Gestor (ADM) e Funcionário."""


def test_qr_funciona_sem_entrar(client):
    assert client.get("/z/sanitario-piso1").status_code == 200
    resp = client.post("/z/sanitario-piso1/conferir", json={"resultado": "ok"})
    assert resp.status_code == 201


def test_funcionario_nao_confirma_nem_ve_painel(client):
    client.post("/entrar/cracha", data={"cracha": "RITA", "perfil": "funcionario"})
    assert client.post("/problemas/1/confirmar", json={}).status_code == 403
    assert client.get("/telas/painel").status_code == 302  # manda entrar como gestor


def test_gestor_entra_e_ve_painel(client):
    resp = client.post("/entrar/cracha", data={"cracha": "otto", "perfil": "gestor"})
    assert resp.status_code == 302
    assert "Otto" in client.get("/telas/painel").get_data(as_text=True)


def test_cracha_errado_ou_perfil_trocado(client):
    assert client.post("/entrar/cracha", data={"cracha": "XYZ", "perfil": "gestor"}).status_code == 400
    assert client.post("/entrar/cracha", data={"cracha": "RITA", "perfil": "gestor"}).status_code == 400


def test_sair(client):
    client.post("/entrar/cracha", data={"cracha": "OTTO", "perfil": "gestor"})
    client.post("/sair")
    assert client.get("/telas/painel").status_code == 302


def test_redirect_so_interno(client):
    resp = client.post("/entrar/cracha", data={"cracha": "OTTO", "perfil": "gestor", "proximo": "//site-malicioso.com"})
    assert "site-malicioso" not in resp.headers["Location"]


def test_tela_de_entrada_tem_sair_para_o_celular(client):
    client.post("/entrar/cracha", data={"cracha": "RITA", "perfil": "funcionario"})
    assert "Sair deste aparelho" in client.get("/entrar").get_data(as_text=True)
