"""Sugestão da IA: categoria, prioridade e equipe a partir do texto da ronda.

Dono: IA (tarefa #6).
Formato da resposta: ver docs/contrato.md (seção 4). Quem decide é o supervisor;
a IA só sugere. Roda offline (sem API paga).
"""
from pathlib import Path

from ia.risco import AVISO_BRIGADA, detectar_risco

ARQUIVO_MODELO = Path(__file__).resolve().parent / "modelo.joblib"


def sugerir(texto: str) -> dict:
    """Recebe o texto da ronda e devolve a sugestão no formato do contrato."""
    risco = detectar_risco(texto)
    # TODO #6: carregar ARQUIVO_MODELO (gerado por ia/treinar.py) e prever de verdade.
    sugestao = {"categoria": "outros", "prioridade": "media", "equipe": "manutencao", "confianca": 0.0}
    if risco:
        sugestao["prioridade"] = "urgente"  # risco nunca baixa a prioridade
    sugestao["risco"] = risco
    sugestao["aviso"] = AVISO_BRIGADA if risco else None
    return sugestao
