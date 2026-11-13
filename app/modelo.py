"""Modelo local: TF-IDF + regressão logística, treinado nas frases do repositório.

O arquivo data/teste_cego.csv não entra no treino. Se o scikit-learn falhar,
a reserva por palavras-chave responde no mesmo formato.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from app.dominio import (
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

_cache: Modelo | None = None


@dataclass(frozen=True)
class Relatorio:
    fonte: str
    treino: int
    teste: int
    acerto_categoria: float
    acerto_baseline: float
    acerto_prioridade: float


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


def _medir(prever, frases: list[dict[str, str]]) -> Relatorio:
    if not frases:
        return Relatorio("vazia", 0, 0, 0.0, 0.0, 0.0)
    categoria_ok = 0
    baseline_ok = 0
    prioridade_ok = 0
    for linha in frases:
        previsto = prever(linha["frase"])
        sugestao = triar(linha["frase"], previsto)
        if previsto.categoria == linha["categoria"]:
            categoria_ok += 1
        if _baseline(linha["frase"]).categoria == linha["categoria"]:
            baseline_ok += 1
        if sugestao.prioridade == linha["prioridade"]:
            prioridade_ok += 1
    total = len(frases)
    return Relatorio(
        fonte="",
        treino=0,
        teste=total,
        acerto_categoria=categoria_ok / total,
        acerto_baseline=baseline_ok / total,
        acerto_prioridade=prioridade_ok / total,
    )


def treinar_palavras() -> Modelo:
    treino = ler_frases(TREINO)
    teste = ler_frases(TESTE)
    relatorio = _medir(_baseline, teste)
    return Modelo(
        "palavras",
        _baseline,
        Relatorio(
            "palavras",
            len(treino),
            relatorio.teste,
            relatorio.acerto_categoria,
            relatorio.acerto_baseline,
            relatorio.acerto_prioridade,
        ),
    )


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

    medido = _medir(prever, teste)
    return Modelo(
        "sklearn",
        prever,
        Relatorio(
            "sklearn",
            len(treino),
            medido.teste,
            medido.acerto_categoria,
            medido.acerto_baseline,
            medido.acerto_prioridade,
        ),
    )


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
