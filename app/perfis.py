"""Perfis da demo: GESTOR (ADM) e FUNCIONÁRIO. Protótipo: crachás fictícios, sem senha.

- Gestor = papel supervisor ou coordenação. Vê o painel e confirma a sugestão da IA.
- Funcionário = encarregado ou manutenção. Faz a ronda (QR), assume e resolve.
- Sem crachá: o QR continua funcionando em 3 toques, registrado como
  "Equipe de campo (sem crachá)". O celular lembra o crachá depois que entra uma vez.
"""

from __future__ import annotations

from flask import session

from app.db import get_db

PAPEIS_GESTOR = frozenset({"supervisor", "coordenacao"})
NOME_PERFIL = {"gestor": "Gestor (ADM)", "funcionario": "Funcionário"}


def perfil_do_papel(papel: str) -> str:
    return "gestor" if papel in PAPEIS_GESTOR else "funcionario"


def usuario_logado() -> dict | None:
    """Usuário que entrou com crachá nesta sessão (ou None)."""
    codigo = session.get("usuario_codigo")
    if not codigo:
        return None
    row = get_db().execute("SELECT * FROM usuarios WHERE codigo = ?", (codigo,)).fetchone()
    if row is None:
        return None
    usuario = dict(row)
    usuario["perfil"] = perfil_do_papel(usuario["papel"])
    usuario["perfil_nome"] = NOME_PERFIL[usuario["perfil"]]
    return usuario


def eh_gestor() -> bool:
    usuario = usuario_logado()
    return bool(usuario and usuario["perfil"] == "gestor")


def buscar_cracha(codigo: str) -> tuple[dict | None, str | None]:
    """Crachá fictício → usuário. Devolve (usuário, erro)."""
    row = get_db().execute(
        """
        SELECT c.ativo, u.* FROM crachas c
        JOIN usuarios u ON u.id = c.usuario_id
        WHERE c.codigo = ?
        """,
        (codigo.strip().upper(),),
    ).fetchone()
    if row is None:
        return None, "Crachá não encontrado."
    if not row["ativo"]:
        return None, "Crachá desativado."
    return dict(row), None


def crachas_demo() -> list[dict]:
    """Lista mostrada na tela de entrada (só dados fictícios)."""
    rows = get_db().execute(
        """
        SELECT c.codigo AS cracha, u.nome, u.funcao, u.papel FROM crachas c
        JOIN usuarios u ON u.id = c.usuario_id
        WHERE c.ativo = 1 ORDER BY u.papel, u.nome
        """
    ).fetchall()
    return [dict(r) | {"perfil": perfil_do_papel(r["papel"])} for r in rows]
