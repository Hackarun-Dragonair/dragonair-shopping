"""Easter Egg da sexta-feira 13: o gato preto na zona.

Ideia: na sexta-feira 13, um gato preto 🐈‍⬛ se esconde na zona que
ninguém confere há MAIS tempo (a mais "esquecida" entre as cinzas).
Quem confere a zona pelo QR espanta o gato, e ele pula para a próxima
zona esquecida. Quando nenhuma zona está cinza, o gato vai embora.

Por que faz parte da solução: é o diferencial da Ronda Viva (a zona
cinza, "o que ninguém conferiu") virando brincadeira. O gato aponta
onde a ronda deve ir primeiro.

Só UMA zona por vez recebe o gato, e a frase aparece uma vez no topo
do mapa (não polui as outras zonas).

Quando aparece (config SEXTA13 ou variável de ambiente SEXTA13):
- "auto" (padrão): só quando a data local é sexta-feira, dia 13
- "1": sempre (para demonstrar em outro dia, ex.: na final de sábado)
- "0": nunca
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

# Palmas não tem horário de verão: UTC-3 fixo (funciona até no Windows sem tzdata).
FUSO = timezone(timedelta(hours=-3))

FRASE = (
    "Sexta-feira 13: um gato preto se esconde na zona que ninguém confere "
    "há mais tempo. Confira a zona para espantá-lo."
)
FRASE_ESPANTOU = "🐈‍⬛ Gato preto espantado! Esta zona não está mais esquecida."


def eh_sexta_13(momento: datetime) -> bool:
    local = momento.astimezone(FUSO)
    return local.weekday() == 4 and local.day == 13


def ativo(momento: datetime | None = None, modo: str = "auto") -> bool:
    modo = (modo or "auto").strip().lower()
    if modo in {"1", "sim", "true", "on"}:
        return True
    if modo in {"0", "nao", "não", "false", "off"}:
        return False
    return eh_sexta_13(momento or datetime.now(timezone.utc))


def zona_do_gato(zonas: list[dict]) -> str | None:
    """Zona cinza conferida há mais tempo. Nunca conferida ganha de todas."""
    cinzas = [z for z in zonas if z["estado"] == "cinza"]
    if not cinzas:
        return None
    # ultima_em vazio ("") = nunca conferida, vem primeiro; empate fica pela ordem do mapa.
    return min(cinzas, key=lambda z: z.get("ultima_em") or "")["codigo"]


def marcar_gato(zonas: list[dict], momento: datetime, modo: str) -> list[dict]:
    codigo = zona_do_gato(zonas) if ativo(momento, modo) else None
    for zona in zonas:
        zona["gato"] = zona["codigo"] == codigo
    return zonas
