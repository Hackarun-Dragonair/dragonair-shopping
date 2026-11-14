"""Front novo: fila em quadro, painel com equipes e mapa interativo."""


def test_fila_em_tres_colunas(client):
    html = client.get("/telas/fila").get_data(as_text=True)
    for coluna in ["Aberto", "Em atendimento", "Resolvidos"]:
        assert coluna in html


def test_painel_tem_equipes_e_etiquetas(client):
    client.post("/entrar", json={"usuario_codigo": "otto"})
    html = client.get("/telas/painel").get_data(as_text=True)
    assert "Problemas abertos por equipe" in html
    assert "/etiquetas.pdf" in html


def test_mapa_carrega_script_e_aviso_de_planta(client):
    html = client.get("/").get_data(as_text=True)
    assert "js/mapa.js" in html
    assert "Editar mapa" in html
