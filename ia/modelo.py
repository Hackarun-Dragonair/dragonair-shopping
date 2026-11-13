"""Sugestão da IA: categoria, prioridade e equipe a partir do texto da ronda.

Dono: IA (tarefa #6).
Formato da resposta: ver docs/contrato.md (seção 4). Quem decide é o supervisor;
a IA só sugere. Roda offline (sem API paga).
Se o modelo ainda não foi treinado, ele é treinado na hora (leva menos de 1 segundo).
"""
import joblib

from ia.risco import AVISO_BRIGADA, detectar_risco
from ia.treinar import ARQUIVO_MODELO, CAMPOS, treinar

ORDEM_PRIORIDADE = ["baixa", "media", "alta", "urgente"]
_cache = {}


def _carregar() -> dict:
    """Carrega o modelo salvo uma vez só (ou treina, se não existir)."""
    if "pacote" not in _cache:
        if not ARQUIVO_MODELO.exists():
            treinar()
        _cache["pacote"] = joblib.load(ARQUIVO_MODELO)
    return _cache["pacote"]


def recarregar() -> None:
    """Esquece o modelo em memória (usar depois de treinar de novo)."""
    _cache.clear()


def sugerir(texto: str) -> dict:
    """Recebe o texto da ronda e devolve a sugestão no formato do contrato."""
    modelos = _carregar()["modelos"]
    sugestao, confiancas = {}, []
    for campo in CAMPOS:
        probabilidades = modelos[campo].predict_proba([texto])[0]
        melhor = probabilidades.argmax()
        sugestao[campo] = str(modelos[campo].classes_[melhor])
        confiancas.append(float(probabilidades[melhor]))
    # Confiança = a do campo menos certo (se um campo está em dúvida, a sugestão toda está).
    sugestao["confianca"] = round(min(confiancas), 2)

    risco = detectar_risco(texto)
    if risco:
        sugestao["prioridade"] = "urgente"  # regra fixa: risco nunca baixa a prioridade
    sugestao["risco"] = risco
    sugestao["aviso"] = AVISO_BRIGADA if risco else None
    return sugestao


def info_modelo() -> dict:
    """Números do treino para a tela 'Sobre a IA'."""
    return _carregar()["metricas"]
