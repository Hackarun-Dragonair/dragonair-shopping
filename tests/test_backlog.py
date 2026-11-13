def test_dossie_traz_prioridade_e_linha_do_tempo(client):
    problema = client.get("/fila").get_json()["problemas"][0]
    corpo = client.get(f"/problemas/{problema['id']}/dossie").get_json()
    assert corpo["prioridade"] == "P3"
    assert corpo["eventos"] >= 1
    assert "Linha do tempo" in corpo["texto"]
    assert "P3" in corpo["texto"]
    texto = client.get(
        f"/problemas/{problema['id']}/dossie",
        headers={"Accept": "text/plain"},
    )
    assert texto.status_code == 200
    assert "Dossiê da ocorrência" in texto.get_data(as_text=True)


def test_dossie_inexistente(client):
    assert client.get("/problemas/9999/dossie").status_code == 404


def test_cracha_so_entra_com_aparelho_autorizado(client, app):
    token = "celular-01"
    recusado = client.post("/crachas/entrar", json={"codigo": "RITA", "token": token})
    assert recusado.status_code == 403
    assert recusado.get_json()["erro"] == "aparelho_nao_autorizado"

    criado = client.post(
        "/dispositivos",
        json={"apelido": "Celular da ronda", "token": token},
    )
    assert criado.status_code == 201
    repetido = client.post(
        "/dispositivos",
        json={"apelido": "Outro nome", "token": token},
    )
    assert repetido.status_code == 200
    assert repetido.get_json()["aparelho"]["novo"] is False

    entrou = client.post("/crachas/entrar", json={"codigo": "rita", "token": token})
    assert entrou.status_code == 200
    assert entrou.get_json()["usuario"]["codigo"] == "rita"
    assert client.post(
        "/crachas/entrar", json={"codigo": "NAOEXISTE", "token": token}
    ).status_code == 404

    with app.app_context():
        from app.db import get_db

        db = get_db()
        db.execute("UPDATE crachas SET ativo = 0 WHERE codigo = 'OTTO'")
        db.commit()
    inativo = client.post("/crachas/entrar", json={"codigo": "OTTO", "token": token})
    assert inativo.status_code == 403
    assert inativo.get_json()["erro"] == "cracha_inativo"
    assert client.post("/dispositivos", json={"apelido": "x", "token": "curto"}).status_code == 400


def test_fila_envio_aplica_uma_vez_e_nao_rebaixa_risco(client):
    resposta = client.post(
        "/fila-envio",
        json={
            "itens": [
                {
                    "chave": "c1",
                    "tipo": "conferencia",
                    "zona": "sanitario-piso1",
                    "resultado": "ok",
                },
                {
                    "chave": "p1",
                    "tipo": "problema",
                    "zona": "doca-1",
                    "descricao": "tem fumaca na doca",
                    "categoria": "seguranca",
                },
            ]
        },
    )
    itens = resposta.get_json()["itens"]
    assert [item["status"] for item in itens] == ["aplicado", "aplicado"]
    assert itens[1]["prioridade"] == "P1"
    assert itens[1]["risco"] is True

    de_novo = client.post(
        "/fila-envio",
        json={
            "itens": [
                {
                    "chave": "c1",
                    "tipo": "conferencia",
                    "zona": "sanitario-piso1",
                    "resultado": "ok",
                }
            ]
        },
    )
    assert de_novo.get_json()["itens"][0]["status"] == "ignorado"
    historico = client.get(
        "/z/sanitario-piso1", headers={"Accept": "application/json"}
    ).get_json()["historico"]
    assert [linha["resultado"] for linha in historico] == ["OK"]
    assert client.post("/fila-envio", json={"itens": []}).status_code == 400


def test_fila_envio_nao_grava_item_invalido(client):
    ruim = client.post(
        "/fila-envio",
        json={
            "itens": [
                {
                    "chave": "ruim",
                    "tipo": "conferencia",
                    "zona": "sanitario-piso1",
                    "resultado": "problema",
                }
            ]
        },
    )
    assert ruim.get_json()["itens"][0]["erro"] == "resultado_invalido"
    certo = client.post(
        "/fila-envio",
        json={
            "itens": [
                {
                    "chave": "ruim",
                    "tipo": "conferencia",
                    "zona": "sanitario-piso1",
                    "resultado": "atencao",
                }
            ]
        },
    )
    assert certo.get_json()["itens"][0]["status"] == "aplicado"


def test_alertas_do_cenario_e_ok_divergente(client):
    corpo = client.get("/alertas").get_json()
    semana = {alerta["codigo"] for alerta in corpo["semana_sem_achados"]}
    assert "entrada-principal" in semana
    assert "corredor-norte" not in semana
    assert "banheiro-l2-norte" not in semana
    assert corpo["ok_divergente"] == []

    client.post("/z/corredor-norte/conferir", json={"resultado": "ok", "origem": "qr"})
    divergentes = {
        alerta["codigo"] for alerta in client.get("/alertas").get_json()["ok_divergente"]
    }
    assert "corredor-norte" in divergentes


def test_ritmo_sugere_sem_trocar_o_prazo_da_zona(client):
    sem = client.get("/zonas/sanitario-piso1/ritmo").get_json()
    assert sem["motivo"] == "sem_historico"
    assert sem["prazo_sugerido"] == sem["prazo_minutos"]

    natal = client.get(
        "/zonas/escada-norte/ritmo?agora=2026-12-25T15:00:00"
    ).get_json()
    assert natal["motivo"] == "evento"
    assert natal["prazo_sugerido"] == natal["prazo_minutos"] // 2

    for _ in range(3):
        client.post("/z/sanitario-piso1/conferir", json={"resultado": "ok"})
    aprendido = client.get("/zonas/sanitario-piso1/ritmo").get_json()
    assert aprendido["motivo"] == "ritmo"
    assert aprendido["prazo_sugerido"] == 15
    assert client.get("/zonas/nao-existe/ritmo").status_code == 404


def test_etiquetas_em_json_e_pdf(client):
    client.post("/entrar", json={"usuario_codigo": "otto"})  # PDF é do gestor
    lista = client.get("/etiquetas").get_json()["etiquetas"]
    assert any(item["codigo"] == "sanitario-piso1" and item["local_qr"] for item in lista)
    pdf = client.get("/etiquetas.pdf")
    assert pdf.status_code == 200
    assert pdf.mimetype == "application/pdf"
    assert pdf.data.startswith(b"%PDF")
    assert b"sanitario-piso1" in pdf.data
