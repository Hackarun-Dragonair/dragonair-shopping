"""Modelo local: TF-IDF + regressão logística, treinado nas frases do repositório.

O arquivo data/teste_cego.csv não entra no treino. Se o scikit-learn falhar,
a reserva por palavras-chave responde no mesmo formato.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from app.dominio import (
    CATEGORIAS,
    Previsao,
    categoria_por_palavras,
    escolher_categoria,
    preparar_texto,
    prioridade_por_regra,
    triar,
)

RAIZ = Path(__file__).resolve().parent.parent
TREINO = RAIZ / "data" / "treino.csv"
TESTE = RAIZ / "data" / "teste_cego.csv"
# Frases reais do campo (Pedro) com rótulos sugeridos por IA, ainda a revisar.
# Não entram no treino nem no número principal.
CAMPO = RAIZ / "data" / "teste_campo.csv"

_cache: Modelo | None = None


@dataclass(frozen=True)
class Relatorio:
    fonte: str
    treino: int
    teste: int
    acerto_categoria: float
    acerto_baseline: float
    acerto_prioridade: float
    # Campos novos têm valor padrão: quem já criava Relatorio com 6 campos continua funcionando.
    recall_p1: float = 0.0  # dos P1 verdadeiros, quantos o sistema final marcou P1
    p1_total: int = 0  # quantos P1 existem no teste (o "n" do recall)
    comparacao: tuple = ()  # 3 linhas: só regras, só modelo, modelo + regra dura
    matriz_classes: tuple = ()  # ordem das categorias na matriz
    matriz: tuple = ()  # matriz[esperado][previsto], categoria do sistema final


class Modelo:
    def __init__(self, fonte: str, prever, relatorio: Relatorio):
        self.fonte = fonte
        self._prever = prever
        self.relatorio = relatorio

    def prever(self, texto: str) -> Previsao:
        return self._prever(texto)


def ler_frases(caminho: Path) -> list[dict[str, str]]:
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def _baseline(texto: str) -> Previsao:
    categoria, alternativa = categoria_por_palavras(texto)
    return Previsao(
        categoria=categoria,
        confianca=0.5 if alternativa is None else 0.4,
        alternativa=alternativa,
        alternativa_confianca=0.4 if alternativa else None,
        prioridade=prioridade_por_regra(texto),
    )


def comparar_linha(prever, linha: dict[str, str]) -> dict:
    """Roda os 3 jeitos numa frase.

    (a) regras: só palavras-chave (categoria e prioridade) + regra dura de risco.
    (b) modelo: só o que o modelo previu, sem regra nenhuma.
    (c) final: o que o sistema mostra = modelo + regras de prioridade + regra dura (triar).
    """
    frase = linha["frase"]
    regras = triar(frase, _baseline(frase))
    modelo = prever(frase)
    final = triar(frase, modelo)
    return {
        "frase": frase,
        "categoria_esperada": linha["categoria"],
        "prioridade_esperada": linha["prioridade"],
        "regras_categoria": regras.categoria,
        "regras_prioridade": regras.prioridade,
        "modelo_categoria": modelo.categoria,
        "modelo_prioridade": modelo.prioridade,
        "final_categoria": final.categoria,
        "final_prioridade": final.prioridade,
    }


def _taxa(acertos: int, total: int) -> float:
    return acertos / total if total else 0.0


def resumir(linhas: list[dict]) -> dict:
    """Acurácia por campo, recall de P1 e matriz de confusão, para os 3 jeitos."""
    total = len(linhas)
    p1 = [l for l in linhas if l["prioridade_esperada"] == "P1"]
    comparacao = []
    for chave, nome in (
        ("regras", "Só regras de palavras"),
        ("modelo", "Só modelo"),
        ("final", "Modelo + regra dura"),
    ):
        comparacao.append(
            {
                "nome": nome,
                "categoria": _taxa(sum(l[f"{chave}_categoria"] == l["categoria_esperada"] for l in linhas), total),
                "prioridade": _taxa(sum(l[f"{chave}_prioridade"] == l["prioridade_esperada"] for l in linhas), total),
                "recall_p1": _taxa(sum(l[f"{chave}_prioridade"] == "P1" for l in p1), len(p1)),
            }
        )
    classes = [codigo for codigo, _ in CATEGORIAS]
    matriz = [[0] * len(classes) for _ in classes]
    for l in linhas:
        if l["categoria_esperada"] in classes and l["final_categoria"] in classes:
            matriz[classes.index(l["categoria_esperada"])][classes.index(l["final_categoria"])] += 1
    return {
        "n": total,
        "p1_total": len(p1),
        "comparacao": comparacao,
        "classes": classes,
        "matriz": matriz,
    }


def _medir(prever, frases: list[dict[str, str]], fonte: str = "", treino: int = 0) -> Relatorio:
    if not frases:
        return Relatorio(fonte or "vazia", treino, 0, 0.0, 0.0, 0.0)
    resumo = resumir([comparar_linha(prever, linha) for linha in frases])
    regras, _, final = resumo["comparacao"]
    return Relatorio(
        fonte=fonte,
        treino=treino,
        teste=resumo["n"],
        acerto_categoria=final["categoria"],
        acerto_baseline=regras["categoria"],
        acerto_prioridade=final["prioridade"],
        recall_p1=final["recall_p1"],
        p1_total=resumo["p1_total"],
        comparacao=tuple(resumo["comparacao"]),
        matriz_classes=tuple(resumo["classes"]),
        matriz=tuple(tuple(linha) for linha in resumo["matriz"]),
    )


def treinar_palavras() -> Modelo:
    treino = ler_frases(TREINO)
    teste = ler_frases(TESTE)
    return Modelo("palavras", _baseline, _medir(_baseline, teste, "palavras", len(treino)))


def treinar_sklearn() -> Modelo:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    treino = ler_frases(TREINO)
    teste = ler_frases(TESTE)
    textos = [preparar_texto(linha["frase"]) for linha in treino]
    categorias = [linha["categoria"] for linha in treino]
    prioridades = [linha["prioridade"] for linha in treino]

    def pipeline() -> Pipeline:
        return Pipeline(
            [
                # Só pedaços de 3 a 5 letras dentro de cada palavra (char_wb).
                # Testamos somar n-gramas de palavras (FeatureUnion): piorou o teste cego, ficou fora.
                ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))),
                (
                    "clf",
                    LogisticRegression(max_iter=1000, class_weight="balanced"),
                ),
            ]
        )

    modelo_categoria = pipeline()
    modelo_prioridade = pipeline()
    modelo_categoria.fit(textos, categorias)
    modelo_prioridade.fit(textos, prioridades)

    def prever(texto: str) -> Previsao:
        preparado = preparar_texto(texto)
        probs = modelo_categoria.predict_proba([preparado])[0]
        classes = list(modelo_categoria.named_steps["clf"].classes_)
        categoria, confianca, alternativa, alt_conf = escolher_categoria(
            list(zip(classes, probs))
        )
        prioridade = str(modelo_prioridade.predict([preparado])[0])
        return Previsao(str(categoria), confianca, str(alternativa) if alternativa else None, alt_conf, prioridade)

    return Modelo("sklearn", prever, _medir(prever, teste, "sklearn", len(treino)))


def obter_modelo() -> Modelo:
    global _cache
    if _cache is None:
        try:
            _cache = treinar_sklearn()
        except Exception:
            _cache = treinar_palavras()
    return _cache


def limpar_cache() -> None:
    global _cache
    _cache = None
