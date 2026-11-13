"""Servidor do Ronda Viva (FastAPI).

Dono: BACKEND (tarefas #2, #3, #11, #12).
Rodar:  uvicorn app.main:app --reload --host 0.0.0.0
Todas as rotas estão listadas em docs/contrato.md (seção 5).
"""
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import banco
from app.status import cor_da_zona
from ia.modelo import sugerir

PASTA_APP = Path(__file__).resolve().parent


@asynccontextmanager
async def ao_ligar(app: FastAPI):
    banco.recriar()  # banco novo com dados de exemplo a cada início
    yield


app = FastAPI(title="Ronda Viva", lifespan=ao_ligar)
app.mount("/static", StaticFiles(directory=PASTA_APP / "static"), name="static")
templates = Jinja2Templates(directory=PASTA_APP / "templates")


def zonas_com_cor() -> list[dict]:
    """Todas as zonas + último registro + cor calculada."""
    with banco.conectar() as con:
        linhas = con.execute("""
            SELECT z.*, r.status AS ultimo_status, r.criado_em AS ultimo_em
            FROM zonas z
            LEFT JOIN registros r ON r.id = (
                SELECT id FROM registros WHERE zona_id = z.id ORDER BY id DESC LIMIT 1)
            ORDER BY z.piso, z.nome""").fetchall()
    agora = datetime.now()
    return [dict(z, cor=cor_da_zona(z["ultimo_status"], z["ultimo_em"], z["prazo_min"], agora)) for z in linhas]


# ---------- Telas ----------

@app.get("/")
def mapa(request: Request):
    return templates.TemplateResponse(request, "mapa.html", {"zonas": zonas_com_cor()})


@app.get("/z/{zona_id}")
def tela_zona(request: Request, zona_id: str, salvo: bool = False):
    with banco.conectar() as con:
        zona = con.execute("SELECT * FROM zonas WHERE id = ?", (zona_id,)).fetchone()
    if zona is None:
        raise HTTPException(404, "Zona não encontrada")
    return templates.TemplateResponse(request, "zona.html", {"zona": zona, "salvo": salvo})


@app.post("/z/{zona_id}")
def salvar_conferencia(zona_id: str, status: str = Form(...), texto: str = Form("")):
    if status not in ("ok", "atencao", "problema"):
        raise HTTPException(400, "Status inválido")
    with banco.conectar() as con:
        con.execute(
            "INSERT INTO registros (zona_id, status, texto, criado_em) VALUES (?, ?, ?, ?)",
            (zona_id, status, texto, banco.agora_iso()),
        )
        # TODO #3: se status != "ok", criar a ocorrência com sugerir(texto)
        #          e registrar o primeiro evento ("criada") na tabela eventos.
    return RedirectResponse(f"/z/{zona_id}?salvo=true", status_code=303)


@app.get("/fila")
def fila(request: Request):
    # TODO #11: listar ocorrências (urgente primeiro) e permitir mudar o estado.
    return templates.TemplateResponse(request, "fila.html", {"ocorrencias": []})


@app.get("/ocorrencias/{ocorrencia_id}")
def ocorrencia(request: Request, ocorrencia_id: int):
    # TODO #12: buscar a ocorrência e seus eventos (linha do tempo) + dossiê.
    return templates.TemplateResponse(request, "ocorrencia.html", {"ocorrencia": None, "eventos": []})


@app.get("/painel")
def painel(request: Request):
    # TODO #4: indicadores por zona e por equipe (nunca por pessoa).
    return templates.TemplateResponse(request, "painel.html", {})


@app.get("/sobre-modelo")
def sobre_modelo(request: Request):
    # TODO #6: mostrar como a IA foi treinada e a taxa de acerto.
    return templates.TemplateResponse(request, "sobre_modelo.html", {})


# ---------- API (JSON) ----------

@app.get("/api/sugestao")
def api_sugestao(texto: str):
    return sugerir(texto)


@app.get("/api/zonas")
def api_zonas():
    return zonas_com_cor()
