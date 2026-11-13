"""Treina a IA com dados/frases.csv e salva em ia/modelo.joblib.

Dono: IA (tarefa #6).  Rodar com:  python -m ia.treinar

Como funciona (para explicar à banca em 1 minuto):
1. Cada frase vira números com TF-IDF: palavras inteiras + pedaços de 3 a 5 letras
   (os pedaços ajudam com erro de digitação, ex.: "entupdo").
2. Uma Regressão Logística aprende, para cada campo (categoria, prioridade, equipe),
   quais palavras indicam cada valor.
3. Medimos o acerto em frases que o modelo NÃO viu no treino (validação cruzada) e
   comparamos com um "chute" que sempre responde o valor mais comum.
"""
import csv
import json
from collections import Counter
from pathlib import Path

import joblib
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import warnings

from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline, make_union

from ia.risco import normalizar

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVO_FRASES = RAIZ / "dados" / "frases.csv"
ARQUIVO_MODELO = Path(__file__).resolve().parent / "modelo.joblib"
CAMPOS = ["categoria", "prioridade", "equipe"]


def ler_frases() -> list[dict]:
    with open(ARQUIVO_FRASES, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def novo_modelo():
    """TF-IDF (palavras + pedaços de palavra) seguido de Regressão Logística."""
    texto = make_union(
        TfidfVectorizer(preprocessor=normalizar, ngram_range=(1, 2)),
        TfidfVectorizer(preprocessor=normalizar, analyzer="char_wb", ngram_range=(3, 5)),
    )
    return make_pipeline(texto, LogisticRegression(max_iter=2000, class_weight="balanced"))


def medir_acerto(textos, rotulos) -> dict:
    """Acerto em frases que o modelo não viu, comparado com o chute.

    Usa validação cruzada: divide as frases em partes, treina com todas menos uma
    e testa na que ficou de fora, repetindo para cada parte. É mais justo que um
    teste só quando temos poucas frases.
    """
    menor_grupo = min(Counter(rotulos).values())
    partes = min(5, menor_grupo)
    if partes >= 2:
        divisao = StratifiedKFold(n_splits=partes, shuffle=True, random_state=42)
    else:  # algum valor aparece uma vez só: divisão simples
        divisao = KFold(n_splits=min(5, len(textos)), shuffle=True, random_state=42)
    modelo = cross_val_score(novo_modelo(), textos, rotulos, cv=divisao).mean()
    chute = cross_val_score(DummyClassifier(strategy="most_frequent"), textos, rotulos, cv=divisao).mean()
    return {"acerto_modelo": round(float(modelo), 2), "acerto_chute": round(float(chute), 2),
            "partes_validacao": divisao.get_n_splits()}


def treinar() -> dict:
    """Treina um modelo por campo com TODAS as frases, mede e salva. Devolve as métricas."""
    warnings.filterwarnings("ignore", category=UserWarning)  # avisos de poucas frases por grupo
    frases = ler_frases()
    textos = [f["texto"] for f in frases]
    modelos, metricas = {}, {"total_frases": len(frases), "campos": {}}
    for campo in CAMPOS:
        rotulos = [f[campo] for f in frases]
        metricas["campos"][campo] = medir_acerto(textos, rotulos)
        modelos[campo] = novo_modelo().fit(textos, rotulos)
    joblib.dump({"modelos": modelos, "metricas": metricas}, ARQUIVO_MODELO)
    return metricas


def main() -> None:
    metricas = treinar()
    print(f"Treinado com {metricas['total_frases']} frases. Salvo em {ARQUIVO_MODELO.name}")
    print(json.dumps(metricas["campos"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
