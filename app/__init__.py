"""Aplicação Ronda Viva. A fábrica lê a configuração e semeia o cenário fictício."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix

from app.db import banco_vazio, fechar_db, get_db, init_db
from app.modelo import obter_modelo
from app.rotas import registrar
from app.rotas.comum import quer_json
from app.seed import semear


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    raiz = Path(app.root_path).parent
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "demo-ronda-viva"),
        DATABASE=os.environ.get("DATABASE_PATH", str(raiz / "instance" / "ronda.sqlite3")),
        SEED_ON_START=os.environ.get("SEED_ON_START", "1") == "1",
        PUBLIC_BASE_URL=os.environ.get("PUBLIC_BASE_URL", "").strip(),
        CORS_ORIGIN=os.environ.get("CORS_ORIGIN", "*"),
        # Easter Egg sexta-feira 13: "auto" (só na data), "1" (sempre, para a demo), "0" (desliga).
        SEXTA13=os.environ.get("SEXTA13", "auto"),
        PERMANENT_SESSION_LIFETIME=60 * 60 * 12,  # o celular lembra o crachá por 12 h
        # Recusa envio maior que 9 MB antes de ler o arquivo (a planta aceita até 8 MB).
        MAX_CONTENT_LENGTH=9 * 1024 * 1024,
    )
    if config:
        app.config.update(config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.teardown_appcontext(fechar_db)

    with app.app_context():
        init_db()
        if app.config["SEED_ON_START"] or banco_vazio():
            semear(get_db())
        modelo = obter_modelo()
        relatorio = modelo.relatorio
        app.logger.info(
            "Modelo %s — categoria %.0f%%, palavras %.0f%%, prioridade %.0f%% (n=%s)",
            modelo.fonte,
            relatorio.acerto_categoria * 100,
            relatorio.acerto_baseline * 100,
            relatorio.acerto_prioridade * 100,
            relatorio.teste,
        )

    registrar(app)

    @app.before_request
    def preflight():
        if request.method == "OPTIONS":
            return "", 204

    @app.after_request
    def cors(resposta):
        resposta.headers["Access-Control-Allow-Origin"] = app.config.get("CORS_ORIGIN", "*")
        resposta.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Usuario"
        resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return resposta

    @app.errorhandler(413)
    def grande_demais(_erro):
        # Arquivo acima do limite: responde em JSON para a tela mostrar a mensagem certa.
        return jsonify(erro="arquivo_grande", mensagem="Imagem maior que 8 MB."), 413

    @app.errorhandler(404)
    def nao_encontrado(_erro):
        # Navegador (QR errado, link velho) vê uma página; a API continua em JSON.
        if "text/html" in request.headers.get("Accept", "") and not quer_json():
            return render_template("nao_encontrado.html"), 404
        return jsonify(erro="nao_encontrado"), 404

    return app
