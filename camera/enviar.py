"""Manda um JSON para a Ronda Viva. Só biblioteca padrão (sem requests)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


def postar(base: str, caminho: str, dados: dict) -> dict:
    corpo = json.dumps(dados).encode("utf-8")
    pedido = urllib.request.Request(
        base.rstrip("/") + caminho,
        data=corpo,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    chave = os.environ.get("CAMERA_CHAVE")
    if chave:
        pedido.add_header("X-Chave-Camera", chave)
    try:
        with urllib.request.urlopen(pedido, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        return {"erro": f"HTTP {erro.code}", "detalhe": erro.read().decode("utf-8", "ignore")}
    except urllib.error.URLError as erro:
        return {"erro": "sem_conexao", "detalhe": str(erro.reason)}
