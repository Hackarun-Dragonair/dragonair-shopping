from app.rotas.mapa import bp as mapa_bp
from app.rotas.painel import bp as painel_bp
from app.rotas.problemas import bp as problemas_bp
from app.rotas.saude import bp as saude_bp
from app.rotas.zona import bp as zona_bp


def registrar(app) -> None:
    app.register_blueprint(saude_bp)
    app.register_blueprint(zona_bp)
    app.register_blueprint(problemas_bp)
    app.register_blueprint(mapa_bp)
    app.register_blueprint(painel_bp)
