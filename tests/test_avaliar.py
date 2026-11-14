import csv

from app.avaliar import f1_macro, gerar
from app.dominio import preparar_texto
from app.modelo import CAMPO, TESTE, TREINO, ler_frases, obter_modelo


def test_avaliar_gera_os_arquivos(tmp_path):
    resultado = gerar(tmp_path)
    for nome in ("avaliacao_teste_cego.csv", "avaliacao_teste_campo.csv", "resumo.md"):
        assert (tmp_path / nome).exists(), nome
    with (tmp_path / "avaliacao_teste_cego.csv").open(encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert len(linhas) == resultado["cego"]["n"] == len(ler_frases(TESTE))
    assert {"frase", "categoria_esperada", "categoria_prevista", "acertou"} <= set(linhas[0])
    resumo = (tmp_path / "resumo.md").read_text(encoding="utf-8")
    assert "Recall de P1" in resumo
    assert "rótulos a revisar" in resumo
    assert "Modelo + regra dura" in resumo


def test_recall_p1_com_regra_dura_e_100_no_teste_cego(tmp_path):
    resultado = gerar(tmp_path)
    regras, modelo, final = resultado["cego"]["comparacao"]
    assert resultado["cego"]["p1_total"] > 0
    assert final["recall_p1"] == 1.0
    # A regra dura só sobe a prioridade: nunca perde P1 que o modelo achou.
    assert final["recall_p1"] >= modelo["recall_p1"]


def test_relatorio_do_boot_tem_recall_e_comparacao():
    r = obter_modelo().relatorio
    assert r.recall_p1 == 1.0
    assert len(r.comparacao) == 3
    assert sum(sum(linha) for linha in r.matriz) == r.teste


def test_teste_campo_fora_do_treino_e_do_teste_cego():
    campo = {preparar_texto(l["frase"]) for l in ler_frases(CAMPO)}
    treino = {preparar_texto(l["frase"]) for l in ler_frases(TREINO)}
    cego = {preparar_texto(l["frase"]) for l in ler_frases(TESTE)}
    assert campo and campo.isdisjoint(treino) and campo.isdisjoint(cego)


def test_f1_macro():
    assert f1_macro(["a", "b"], ["a", "b"]) == 1.0
    assert f1_macro(["a", "b"], ["b", "a"]) == 0.0
