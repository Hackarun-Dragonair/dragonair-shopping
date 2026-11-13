"""Detecta situações de risco no texto da ronda.

Dono: IA (tarefa #7).
Regra do projeto: se houver risco, o sistema SEMPRE mostra "Avise a brigada pelo rádio"
e a prioridade NUNCA é rebaixada. O sistema não chama ninguém sozinho.
"""

PALAVRAS_RISCO = ["fumaça", "fogo", "incêndio", "choque", "faísca", "pessoa presa", "desmaio"]

AVISO_BRIGADA = "Avise a brigada pelo rádio."


def detectar_risco(texto: str) -> bool:
    """True se o texto tiver alguma palavra de risco."""
    # TODO #7: ignorar maiúsculas/acentos e devolver True quando achar uma palavra de PALAVRAS_RISCO.
    return False
