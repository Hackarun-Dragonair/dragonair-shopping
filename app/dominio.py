"""Regras da ronda que não dependem de banco nem de HTTP.

A prioridade de risco (fumaça, fogo, gás, choque, pessoa presa) sai daqui,
antes do modelo. O modelo pode sugerir; esta camada não deixa rebaixar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta

CATEGORIAS: tuple[tuple[str, str], ...] = (
    ("hidraulica", "Hidráulica"),
    ("eletrica", "Elétrica"),
    ("climatizacao", "Climatização"),
    ("limpeza", "Limpeza"),
    ("seguranca", "Segurança"),
    ("estrutura", "Estrutura"),
)

PRIORIDADES: tuple[str, ...] = ("P1", "P2", "P3", "P4")

AVISO_BRIGADA = (
    "Avise a brigada pelo rádio. O sistema não aciona ninguém "
    "e não rebaixa este risco."
)

_ACENTOS = str.maketrans(
    "áàâãäéèêëíìîïóòôõöúùûüç",
    "aaaaaeeeeiiiiooooouuuuc",
)

# Casos combinados pela equipe (gás incluído no sábado 14/11, depois da banca simulada;
# só "água com gás", "refri sem gás" e "refrigerante sem gás" não contam;
# qualquer outro "gás", até "cozinha com gás vazando", aciona a brigada).
# Faísca e alagamento sobem a prioridade pelas regras abaixo, sem o aviso de brigada.
_RISCO = re.compile(
    r"\bfumaca\b|\bfogo\b|\bincendio\b|(?<!agua com )(?<!refri sem )(?<!refrigerante sem )\bgas\b|\bchoque\b|\beletrocut"
    r"|\bpessoa presa\b|\bgente presa\b|\balguem preso\b"
    r"|\bpreso no elevador\b|\bpresa no elevador\b"
)

_ORDEM_PRIORIDADE = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}

# Desempate do classificador por palavras: empate fica com a primeira.
_PALAVRAS: dict[str, tuple[str, ...]] = {
    "hidraulica": (
        "ping", "vaz", "cano", "agua", "torneira", "entup", "goteira",
        "infiltra", "ralo", "vaso", "privada", "jorr",
    ),
    "eletrica": (
        "luz", "lampada", "tomada", "disjuntor", "eletr", "faisca",
        "centelha", "energia", "queimado", "escuro", "pisca",
    ),
    "climatizacao": (
        "ar cond", "climat", "vento", "quente", "duto", "grelha", "gelad",
    ),
    "limpeza": (
        "lixo", "lixeira", "suj", "papel", "cheiro", "fed", "sabonete",
        "grudent", "mesa", "molhado",
    ),
    "seguranca": (
        "extintor", "camera", "emergencia", "alarme", "portao",
        "estranha", "travad", "grade", "doca aberta", "fumaca", "fogo",
    ),
    "estrutura": (
        "quebr", "rachad", "azulejo", "corrimao", "forro", "vidro",
        "degrau", "bambo", "pendur", "afund", "solta", "solto",
    ),
}

BOTOES_POR_TIPO: dict[str, tuple[str, ...]] = {
    "sanitario": (
        "Piso molhado",
        "Vaso entupido",
        "Sem papel",
        "Sem luz",
        "Mau cheiro",
    ),
    "praca_alimentacao": (
        "Piso molhado",
        "Lixo cheio",
        "Mesa suja",
        "Cadeira quebrada",
    ),
    "corredor": (
        "Lâmpada queimada",
        "Piso molhado",
        "Está pingando do teto",
    ),
    "escada": ("Escada parada", "Degrau solto", "Sem luz"),
    "doca": ("Porta aberta", "Piso molhado", "Lixo acumulado"),
    "entrada": ("Porta com defeito", "Piso molhado", "Sem luz"),
    "estacionamento": ("Lâmpada queimada", "Poça de água", "Portão aberto"),
    "area_tecnica": ("Vazamento", "Quadro aberto", "Cheiro de queimado"),
}

PERTO_DE: tuple[tuple[str, str], ...] = (
    ("saida_de_ar", "saída de ar"),
    ("cano", "cano"),
    ("quadro", "quadro"),
    ("teto", "teto"),
    ("outro", "outro"),
)

ESTADOS = {
    "ok": "OK",
    "atencao": "Atenção",
    "problema": "Problema",
    "cinza": "Sem conferência",
}


def preparar_texto(texto: str) -> str:
    limpo = texto.lower().translate(_ACENTOS)
    limpo = re.sub(r"[^a-z0-9\s]", " ", limpo)
    return re.sub(r"\s+", " ", limpo).strip()


def nome_categoria(codigo: str) -> str:
    for chave, nome in CATEGORIAS:
        if chave == codigo:
            return nome
    return codigo


def detectar_risco(texto: str) -> bool:
    return _RISCO.search(preparar_texto(texto)) is not None


def prioridade_por_regra(texto: str) -> str:
    t = preparar_texto(texto)
    # Peça pendurada e saída de emergência bloqueada sobem para P1.
    # Não disparam o aviso de brigada — esse aviso continua só nas palavras de risco.
    if "emergencia" in t and any(p in t for p in ("travad", "bloque", "nao abre")):
        return "P1"
    if any(p in t for p in ("pendur",)):
        return "P1"
    if any(p in t for p in ("alag", "sem luz", "sem nenhuma luz", "escuro", "faisca", "centelha", "forro caindo")):
        return "P2"
    if any(p in t for p in ("ping", "vaz", "entup", "quebr", "parad", "jorr", "travad")):
        return "P2"
    if any(p in t for p in ("suj", "lixo", "cheiro", "fed", "papel")):
        return "P3"
    return "P4"


def mais_urgente(a: str, b: str) -> str:
    if _ORDEM_PRIORIDADE.get(a, 9) <= _ORDEM_PRIORIDADE.get(b, 9):
        return a
    return b


def garantir_prioridade(texto: str, prioridade: str) -> tuple[str, bool]:
    """Devolve a prioridade final e se houve palavra de risco.

    Palavra de risco fica em P1 mesmo que alguém tente gravar P2, P3 ou P4.
    """
    risco = detectar_risco(texto)
    if risco:
        return "P1", True
    if prioridade not in _ORDEM_PRIORIDADE:
        return "P4", False
    return prioridade, False


def categoria_por_palavras(texto: str) -> tuple[str, str | None]:
    t = preparar_texto(texto)
    pontos = []
    for categoria, palavras in _PALAVRAS.items():
        pontos.append((sum(1 for p in palavras if p in t), categoria))
    pontos.sort(key=lambda item: item[0], reverse=True)
    melhor, segundo = pontos[0], pontos[1]
    if melhor[0] == 0:
        return "estrutura", None
    alternativa = segundo[1] if segundo[0] > 0 and melhor[0] - segundo[0] <= 0 else None
    return melhor[1], alternativa


def escolher_categoria(
    pares: list[tuple[str, float]],
    margem: float = 0.12,
) -> tuple[str, float, str | None, float | None]:
    """Escolhe a categoria e, se as duas primeiras quase empatam, a segunda."""
    ordenados = sorted(pares, key=lambda item: item[1], reverse=True)
    categoria, confianca = ordenados[0]
    if len(ordenados) == 1 or ordenados[0][1] - ordenados[1][1] >= margem:
        return categoria, float(confianca), None, None
    return categoria, float(confianca), ordenados[1][0], float(ordenados[1][1])


@dataclass(frozen=True)
class Previsao:
    categoria: str
    confianca: float
    alternativa: str | None
    alternativa_confianca: float | None
    prioridade: str


@dataclass(frozen=True)
class Sugestao:
    categoria: str
    categoria_nome: str
    prioridade: str
    confianca: float
    alternativa: str | None
    alternativa_nome: str | None
    alternativa_confianca: float | None
    risco: bool
    aviso: str | None


def triar(texto: str, previsao: Previsao) -> Sugestao:
    risco = detectar_risco(texto)
    prioridade = mais_urgente(previsao.prioridade, prioridade_por_regra(texto))
    if risco:
        prioridade = "P1"
    return Sugestao(
        categoria=previsao.categoria,
        categoria_nome=nome_categoria(previsao.categoria),
        prioridade=prioridade,
        confianca=previsao.confianca,
        alternativa=previsao.alternativa,
        alternativa_nome=nome_categoria(previsao.alternativa) if previsao.alternativa else None,
        alternativa_confianca=previsao.alternativa_confianca,
        risco=risco,
        aviso=AVISO_BRIGADA if risco else None,
    )


def estado_da_zona(
    *,
    ultimo_resultado: str | None,
    ultima_em: datetime | None,
    prazo_minutos: int,
    problema_aberto: bool,
    agora: datetime,
) -> str:
    """Problema aberto permanece visível. Sem conferência no prazo, a zona fica cinza."""
    if problema_aberto:
        return "problema"
    if ultima_em is None or agora - ultima_em > timedelta(minutes=prazo_minutos):
        return "cinza"
    if ultimo_resultado == "atencao":
        return "atencao"
    return "ok"


def ha_quanto(momento: datetime | None, agora: datetime) -> str:
    if momento is None:
        return "ninguém conferiu"
    minutos = int((agora - momento).total_seconds() // 60)
    if minutos < 1:
        return "agora há pouco"
    if minutos < 60:
        return f"há {minutos} min"
    horas = minutos // 60
    if horas < 48:
        return f"há {horas} h"
    return f"há {horas // 24} dias"
