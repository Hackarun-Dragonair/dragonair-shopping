"""Resumo imprimível de uma ocorrência. Não desenha tela."""

from __future__ import annotations

from app.dominio import AVISO_BRIGADA


def texto_dossie(problema: dict) -> str:
    risco = "sim" if problema["risco"] else "não"
    linhas = [
        "Dossiê da ocorrência",
        f"Zona: {problema['zona_nome']} ({problema['piso']})",
        f"Onde colar o QR: {problema['local_qr']}",
        f"Descrição: {problema['descricao']}",
        f"Categoria: {problema['categoria_nome']}",
        f"Prioridade: {problema['prioridade']}",
        f"Equipe: {problema['equipe_nome']}",
        f"Status: {problema['status_nome']}",
        f"Aberto em: {problema['quando']}",
        f"Risco: {risco}",
    ]
    if problema["risco"]:
        linhas.append(AVISO_BRIGADA)
    if problema["resolvido_quando"]:
        linhas.append(f"Resolvido em: {problema['resolvido_quando']}")
    linhas.append("")
    linhas.append("Linha do tempo")
    for evento in problema["eventos"]:
        linhas.append(f"- {evento['quando']} · {evento['texto']}")
    linhas.append("")
    linhas.append("Este histórico só recebe eventos novos. Nada aqui foi apagado.")
    return "\n".join(linhas)
