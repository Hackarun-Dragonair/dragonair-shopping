"""As telas abrem no navegador e mostram os dados certos."""


def test_telas_abrem(client):
    client.post("/entrar", json={"usuario_codigo": "otto"})  # painel é do gestor
    for rota in ["/", "/z/sanitario-piso1", "/telas/fila", "/telas/painel", "/telas/sobre-a-ia"]:
        resposta = client.get(rota)
        assert resposta.status_code == 200, rota
        assert "text/html" in resposta.content_type, rota


def test_mapa_mostra_zona_cinza(client):
    html = client.get("/").get_data(as_text=True)
    assert "estado-cinza" in html
    assert "Ninguém conferiu" in html


def test_fluxo_problema_aparece_na_fila_e_na_tela(client):
    criado = client.post(
        "/z/sanitario-piso1/problema",
        json={"descricao": "fumaça saindo da tomada", "categoria": "eletrica", "origem": "qr"},
    ).get_json()
    pid = criado["problema"]["id"]
    assert "brigada" in criado["aviso"]
    assert "fumaça saindo da tomada" in client.get("/telas/fila").get_data(as_text=True)
    tela = client.get(f"/telas/problemas/{pid}").get_data(as_text=True)
    assert "Linha do tempo" in tela and "Avise a brigada" in tela


def test_problema_inexistente(client):
    assert client.get("/telas/problemas/9999").status_code == 404


def test_qr_errado_mostra_pagina_no_navegador(client):
    navegador = client.get("/z/zona-que-nao-existe", headers={"Accept": "text/html"})
    assert navegador.status_code == 404
    assert "Não achamos esta página" in navegador.get_data(as_text=True)
    api = client.get("/z/zona-que-nao-existe", headers={"Accept": "application/json"})
    assert api.status_code == 404 and api.get_json() == {"erro": "nao_encontrado"}


def test_api_continua_em_json(client):
    assert client.get("/mapa").is_json
    assert client.get("/fila").is_json
