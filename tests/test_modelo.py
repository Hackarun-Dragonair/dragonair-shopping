from app.dominio import preparar_texto
from app.modelo import ler_frases, treinar_sklearn, TESTE, TREINO


def test_teste_cego_nao_entra_no_treino():
    treino = {preparar_texto(linha["frase"]) for linha in ler_frases(TREINO)}
    teste = {preparar_texto(linha["frase"]) for linha in ler_frases(TESTE)}
    assert treino.isdisjoint(teste)
    assert len(teste) >= 15


def test_modelo_mede_o_teste_cego():
    modelo = treinar_sklearn()
    relatorio = modelo.relatorio
    assert relatorio.fonte == "sklearn"
    assert relatorio.teste >= 15
    assert relatorio.acerto_categoria >= 0.8
    assert relatorio.acerto_prioridade >= 0.8
    fumaca = modelo.prever("vi fumaça perto da praça")
    assert fumaca.categoria
