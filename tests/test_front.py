"""Front novo: fila em quadro, painel com equipes e mapa interativo."""


def test_fila_em_tres_colunas(client):
    html = client.get("/telas/fila").get_data(as_text=True)
    for coluna in ["Abertas", "Em atendimento", "Resolvidas"]:
        assert coluna in html


def test_painel_tem_equipes_e_etiquetas(client):
    client.post("/entrar", json={"usuario_codigo": "otto"})
    html = client.get("/telas/painel").get_data(as_text=True)
    assert "Ocorrências abertas por equipe" in html
    assert "/etiquetas.pdf" in html


def test_mapa_carrega_script_e_aviso_de_planta(client):
    html = client.get("/").get_data(as_text=True)
    assert "js/mapa.js" in html
    assert "Editar mapa" in html
    assert 'id="sem-lugar"' in html  # zonas ainda não pintadas na planta não somem
