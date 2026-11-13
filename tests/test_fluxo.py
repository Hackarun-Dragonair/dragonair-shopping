def test_saude(client):
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


def test_respostas_sao_json(client):
    resposta = client.get("/mapa")
    assert resposta.status_code == 200
    assert resposta.is_json
    assert "<html" not in resposta.get_data(as_text=True).lower()


def test_mapa_marca_zona_cinza(client):
    dados = client.get("/mapa").get_json()
    estados = {zona["codigo"]: zona["estado"] for zona in dados["zonas"]}
    assert estados["banheiro-l1-sul"] == "cinza"
    assert estados["praca-a"] == "cinza"
    assert estados["banheiro-l2-norte"] == "ok"
    assert estados["corredor-norte"] == "problema"
    assert dados["cinza"] == 5
    assert dados["zonas"][0]["url"].startswith("http")


def test_ok_tira_a_zona_do_cinza(client):
    resposta = client.post(
        "/z/banheiro-l1-sul/conferir",
        json={"resultado": "ok", "origem": "qr"},
    )
    assert resposta.status_code == 201
    estados = {
        zona["codigo"]: zona["estado"]
        for zona in client.get("/mapa").get_json()["zonas"]
    }
    assert estados["banheiro-l1-sul"] == "ok"


def test_frase_de_vazamento_sugere_hidraulica_e_entra_na_fila(client):
    triagem = client.post(
        "/z/banheiro-l2-norte/triagem",
        json={"descricao": "está pingando do teto do banheiro", "origem": "qr"},
    )
    assert triagem.status_code == 200
    assert triagem.get_json()["sugestao"]["categoria"] == "hidraulica"
    assert triagem.get_json()["equipe_nome"] == "Manutenção"

    criado = client.post(
        "/z/banheiro-l2-norte/problema",
        json={
            "descricao": "está pingando do teto do banheiro",
            "origem": "qr",
            "categoria": "hidraulica",
            "perto_de": "teto",
        },
    )
    assert criado.status_code == 201
    problema = criado.get_json()["problema"]
    assert "pingando do teto" in problema["descricao"]
    assert problema["confirmado"] == 0
    fila = client.get("/fila").get_json()["problemas"]
    assert any("pingando do teto" in item["descricao"] for item in fila)


def test_fumaca_permanece_p1_se_tentarem_rebaixar(client, app):
    with app.app_context():
        from app.db import get_db

        equipe = get_db().execute(
            "SELECT id FROM equipes WHERE codigo = 'seguranca'"
        ).fetchone()["id"]

    resposta = client.post(
        "/z/praca-a/problema",
        json={
            "descricao": "tem fumaça na praça de alimentação",
            "origem": "lista",
            "categoria": "seguranca",
            "editado": "1",
            "prioridade": "P4",
            "equipe_id": equipe,
            "sugestao_categoria": "seguranca",
            "sugestao_prioridade": "P1",
        },
    )
    body = resposta.get_json()
    assert resposta.status_code == 201
    assert body["problema"]["prioridade"] == "P1"
    assert body["problema"]["risco"] == 1
    assert body["problema"]["origem"] == "lista"
    assert "rebaixada" in body["aviso"]
    assert any("brigada" in evento["texto"] for evento in body["problema"]["eventos"])


def test_supervisor_confirma_e_a_linha_do_tempo_so_cresce(client, app):
    assert client.post("/entrar", json={"usuario_codigo": "otto"}).status_code == 200
    with app.app_context():
        from app.db import get_db

        problema = get_db().execute(
            """
            SELECT p.id, p.categoria, p.equipe_id
            FROM problemas p
            JOIN zonas z ON z.id = p.zona_id
            WHERE z.codigo = 'corredor-norte'
            """
        ).fetchone()
        antes = get_db().execute(
            "SELECT COUNT(*) AS n FROM eventos WHERE problema_id = ?",
            (problema["id"],),
        ).fetchone()["n"]

    confirmado = client.post(
        f"/problemas/{problema['id']}/confirmar",
        json={
            "categoria": problema["categoria"],
            "prioridade": "P2",
            "equipe_id": problema["equipe_id"],
        },
    )
    textos = " ".join(evento["texto"] for evento in confirmado.get_json()["problema"]["eventos"])
    assert "confirmou" in textos

    resolvido = client.post(f"/problemas/{problema['id']}/resolver")
    assert resolvido.get_json()["problema"]["status"] == "resolvido"
    with app.app_context():
        from app.db import get_db

        depois = get_db().execute(
            "SELECT COUNT(*) AS n FROM eventos WHERE problema_id = ?",
            (problema["id"],),
        ).fetchone()["n"]
    assert depois > antes


def test_painel_nao_ranqueia_pessoa(app):
    with app.app_context():
        from app.consultas import indicadores
        from app.db import get_db

        dados = indicadores(get_db())
    assert dados["zonas_no_prazo_pct"] == 55
    assert dados["zonas_cinza"] == 5
    assert dados["reincidencia"] == 1
    assert "usuario" not in dados
    assert "Rita" not in str(dados)


def test_pagina_inicial_abre(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "text/html" in resposta.content_type
    assert "Ronda Viva" in resposta.get_data(as_text=True)
    assert "Sanitário piso 1" in resposta.get_data(as_text=True)


def test_qr_sanitario_piso1_registra_ok(client, app):
    pagina = client.get("/z/sanitario-piso1")
    html = pagina.get_data(as_text=True)
    assert pagina.status_code == 200
    assert "Sanitário piso 1" in html
    assert 'value="ok"' in html
    assert 'value="atencao"' in html
    assert 'value="problema"' in html

    depois = client.post(
        "/z/sanitario-piso1/conferir",
        data={"resultado": "ok", "origem": "qr"},
        follow_redirects=True,
    )
    assert "Conferência OK registrada." in depois.get_data(as_text=True)
    with app.app_context():
        from app.db import get_db

        total = get_db().execute(
            """
            SELECT COUNT(*) AS n
            FROM conferencias c
            JOIN zonas z ON z.id = c.zona_id
            WHERE z.codigo = 'sanitario-piso1' AND c.resultado = 'ok'
            """
        ).fetchone()["n"]
    assert total == 1


def test_zona_inexistente(client):
    resposta = client.get("/z/nao-existe")
    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "nao_encontrado"
