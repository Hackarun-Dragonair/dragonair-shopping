"""Confere se as planilhas seguem docs/contrato.md. Dono: DADOS (tarefas #8 e #9).
Se este teste falhar, ele diz a linha e o valor errado."""
import csv
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados"
TIPOS = {"sanitario", "praca", "corredor", "area_tecnica", "doca", "entrada", "estacionamento"}
CATEGORIAS = {"limpeza", "hidraulica", "eletrica", "climatizacao", "estrutura", "seguranca", "outros"}
PRIORIDADES = {"baixa", "media", "alta", "urgente"}
EQUIPES = {"limpeza", "manutencao", "seguranca"}


def ler(nome):
    with open(DADOS / nome, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_zonas():
    zonas = ler("zonas.csv")
    assert list(zonas[0]) == ["id", "nome", "tipo", "piso", "x", "y", "largura", "altura", "prazo_min"]
    ids = [z["id"] for z in zonas]
    assert len(ids) == len(set(ids)), "id de zona repetido"
    for n, z in enumerate(zonas, start=2):
        assert z["tipo"] in TIPOS, f"linha {n}: tipo '{z['tipo']}' não existe no contrato"
        assert z["id"] == z["id"].lower() and " " not in z["id"], f"linha {n}: id deve ser minúsculo com hífen"
        for campo in ("piso", "x", "y", "largura", "altura", "prazo_min"):
            assert z[campo].isdigit(), f"linha {n}: {campo} deve ser número"


def test_frases():
    frases = ler("frases.csv")
    assert list(frases[0]) == ["texto", "categoria", "prioridade", "equipe"]
    for n, f in enumerate(frases, start=2):
        assert f["categoria"] in CATEGORIAS, f"linha {n}: categoria '{f['categoria']}'"
        assert f["prioridade"] in PRIORIDADES, f"linha {n}: prioridade '{f['prioridade']}'"
        assert f["equipe"] in EQUIPES, f"linha {n}: equipe '{f['equipe']}'"
