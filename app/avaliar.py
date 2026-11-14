"""Gera as evidências da IA em docs/evidencias/modelo/.

Rodar: python -m app.avaliar

1. Treina o modelo só com data/treino.csv (o mesmo do sistema).
2. Mede no teste cego (rótulos da equipe, sem IA) e, numa seção separada,
   no teste de campo (frases reais, rótulos sugeridos por IA, a revisar).
3. Escreve um CSV por frase e um resumo.md com acurácia, recall de P1,
   matriz de confusão e a comparação regras x modelo x modelo + regra dura.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.dominio import nome_categoria
from app.modelo import CAMPO, RAIZ, TESTE, comparar_linha, ler_frases, resumir, treinar_sklearn

SAIDA = RAIZ / "docs" / "evidencias" / "modelo"

COLUNAS = [
    "frase",
    "categoria_esperada",
    "categoria_prevista",
    "prioridade_esperada",
    "prioridade_prevista",
    "acertou_categoria",
    "acertou_prioridade",
    "acertou",
]


def _pct(valor: float) -> str:
    return f"{valor * 100:.0f}%"


def f1_macro(esperados: list[str], previstos: list[str]) -> float:
    """Média do F1 de cada classe que aparece no teste (cada classe pesa igual)."""
    classes = sorted(set(esperados))
    if not classes:
        return 0.0
    soma = 0.0
    for c in classes:
        vp = sum(e == c and p == c for e, p in zip(esperados, previstos))
        fp = sum(e != c and p == c for e, p in zip(esperados, previstos))
        fn = sum(e == c and p != c for e, p in zip(esperados, previstos))
        soma += 2 * vp / (2 * vp + fp + fn) if vp else 0.0
    return soma / len(classes)


def escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    """Uma linha por frase, com o que o sistema final (modelo + regra dura) respondeu."""
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        for l in linhas:
            cat_ok = l["final_categoria"] == l["categoria_esperada"]
            pri_ok = l["final_prioridade"] == l["prioridade_esperada"]
            escritor.writerow(
                {
                    "frase": l["frase"],
                    "categoria_esperada": l["categoria_esperada"],
                    "categoria_prevista": l["final_categoria"],
                    "prioridade_esperada": l["prioridade_esperada"],
                    "prioridade_prevista": l["final_prioridade"],
                    "acertou_categoria": "sim" if cat_ok else "nao",
                    "acertou_prioridade": "sim" if pri_ok else "nao",
                    "acertou": "sim" if cat_ok and pri_ok else "nao",
                }
            )


def secao(titulo: str, aviso: str, arquivo_csv: str, linhas: list[dict]) -> str:
    """Texto markdown de um conjunto de teste."""
    r = resumir(linhas)
    regras, modelo, final = r["comparacao"]
    f1_cat = f1_macro([l["categoria_esperada"] for l in linhas], [l["final_categoria"] for l in linhas])
    f1_pri = f1_macro([l["prioridade_esperada"] for l in linhas], [l["final_prioridade"] for l in linhas])
    p1_ok = round(final["recall_p1"] * r["p1_total"])
    partes = [
        f"## {titulo}",
        "",
        aviso,
        "",
        f"- **n = {r['n']}** frases (detalhe por frase: `{arquivo_csv}`)",
        f"- Acurácia categoria: **{_pct(final['categoria'])}** (F1 macro {f1_cat:.2f})",
        f"- Acurácia prioridade: **{_pct(final['prioridade'])}** (F1 macro {f1_pri:.2f})",
        f"- Recall de P1: **{_pct(final['recall_p1'])}** ({p1_ok} de {r['p1_total']} P1)",
        "",
        "### Comparação",
        "",
        "| Jeito | Categoria | Prioridade | Recall P1 |",
        "|---|---|---|---|",
    ]
    for linha in (regras, modelo, final):
        partes.append(
            f"| {linha['nome']} | {_pct(linha['categoria'])} | {_pct(linha['prioridade'])} | {_pct(linha['recall_p1'])} |"
        )
    partes += [
        "",
        "(a) só regras: palavras-chave para categoria e prioridade + regra dura de risco, sem modelo. "
        "(b) só modelo: o que o modelo previu, sem regra nenhuma. "
        "(c) modelo + regra dura: o que o sistema mostra (`triar`); a prioridade nunca fica abaixo da regra.",
        "",
        "### Matriz de confusão da categoria (sistema final)",
        "",
        "Linha = rótulo esperado; coluna = previsto.",
        "",
    ]
    nomes = [nome_categoria(c) for c in r["classes"]]
    partes.append("| Esperado \\ Previsto | " + " | ".join(nomes) + " |")
    partes.append("|---" * (len(nomes) + 1) + "|")
    for nome, valores in zip(nomes, r["matriz"]):
        partes.append(f"| {nome} | " + " | ".join(str(v) for v in valores) + " |")
    erros = [l for l in linhas if l["final_categoria"] != l["categoria_esperada"] or l["final_prioridade"] != l["prioridade_esperada"]]
    partes += ["", "### Erros do sistema final", ""]
    if not erros:
        partes.append("Nenhum.")
    for l in erros:
        partes.append(
            f"- \"{l['frase']}\": esperado {l['categoria_esperada']}/{l['prioridade_esperada']}, "
            f"previsto {l['final_categoria']}/{l['final_prioridade']}"
        )
    partes.append("")
    return "\n".join(partes)


def gerar(saida: Path = SAIDA) -> dict:
    """Treina, mede os dois conjuntos e grava os arquivos. Devolve os resumos."""
    saida.mkdir(parents=True, exist_ok=True)
    modelo = treinar_sklearn()
    cego = [comparar_linha(modelo.prever, l) for l in ler_frases(TESTE)]
    campo = [comparar_linha(modelo.prever, l) for l in ler_frases(CAMPO)] if CAMPO.exists() else []

    escrever_csv(saida / "avaliacao_teste_cego.csv", cego)
    escrever_csv(saida / "avaliacao_teste_campo.csv", campo)

    texto = [
        "# Avaliação do modelo (gerado por `python -m app.avaliar`)",
        "",
        f"Modelo: TF-IDF de pedaços de palavra (char_wb, 3 a 5 letras) + Regressão Logística. "
        f"Treinado com {modelo.relatorio.treino} frases de `data/treino.csv`. "
        "Nenhuma frase de teste entra no treino.",
        "",
        secao(
            "Teste cego (número oficial)",
            "`data/teste_cego.csv`: frases escritas e rotuladas à mão pela equipe, sem IA. "
            "É o número que vai para a tela e para o pitch. n pequeno: ler como indicação, não como garantia.",
            "avaliacao_teste_cego.csv",
            cego,
        ),
        secao(
            "Teste de campo (rótulos a revisar)",
            "`data/teste_campo.csv`: **rótulos a revisar.** Frases reais do jeito que a equipe de campo escreve "
            "(Pedro), mas a categoria e a prioridade foram **sugeridas por IA** e ainda não foram revisadas por "
            "duas pessoas. Não conta como teste cego; serve para ver onde o modelo sofre com linguagem real.",
            "avaliacao_teste_campo.csv",
            campo,
        ),
    ]
    (saida / "resumo.md").write_text("\n".join(texto), encoding="utf-8")
    return {"cego": resumir(cego), "campo": resumir(campo)}


if __name__ == "__main__":
    resultado = gerar()
    for nome, r in resultado.items():
        final = r["comparacao"][2]
        print(
            f"{nome}: n={r['n']} categoria={_pct(final['categoria'])} "
            f"prioridade={_pct(final['prioridade'])} recall_P1={_pct(final['recall_p1'])}"
        )
    print(f"Arquivos em {SAIDA}")
