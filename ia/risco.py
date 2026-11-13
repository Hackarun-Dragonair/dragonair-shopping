"""Detecta situações de risco no texto da ronda.

Dono: IA (tarefa #7).
Regra do projeto: se houver risco, o sistema SEMPRE mostra "Avise a brigada pelo rádio"
e a prioridade NUNCA é rebaixada. O sistema não chama ninguém sozinho.
"""
import unicodedata

# Escritas sem acento: o texto também é comparado sem acento.
PALAVRAS_RISCO = [
    "fumaca", "fogo", "incendio", "chama", "queimando", "cheiro de queimado",
    "choque", "faisca", "curto-circuito", "curto circuito",
    "pessoa presa", "preso no elevador", "presa no elevador",
    "desmaio", "desmaiou", "vazamento de gas", "cheiro de gas",
]

AVISO_BRIGADA = "Avise a brigada pelo rádio."


def normalizar(texto: str) -> str:
    """Minúsculo e sem acento: 'Fumaça' vira 'fumaca'."""
    sem_acento = unicodedata.normalize("NFD", texto or "")
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.lower()


def detectar_risco(texto: str) -> bool:
    """True se o texto tiver alguma palavra de risco."""
    t = normalizar(texto)
    return any(palavra in t for palavra in PALAVRAS_RISCO)
