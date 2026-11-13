"""Cor de cada zona no mapa.

Dono: DADOS + TELAS (tarefa #10).
Regra (docs/contrato.md): verde = ok, amarelo = atenção, vermelho = problema,
cinza = ninguém conferiu dentro do prazo da zona.
"""
from datetime import datetime, timedelta

CORES = {"ok": "verde", "atencao": "amarelo", "problema": "vermelho"}


def cor_da_zona(ultimo_status: str | None, ultimo_em: str | None,
                prazo_min: int, agora: datetime) -> str:
    """Devolve 'verde', 'amarelo', 'vermelho' ou 'cinza'."""
    if ultimo_status is None or ultimo_em is None:
        return "cinza"  # nunca foi conferida
    if agora - datetime.fromisoformat(ultimo_em) > timedelta(minutes=int(prazo_min)):
        return "cinza"  # passou do prazo sem ninguém conferir
    return CORES.get(ultimo_status, "cinza")
