import os
from flask import Flask
from devcontrol.database.db import create_tables

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

    # CRIA AS TABELAS
    create_tables()

    # IMPORTA BLUEPRINTS
    from devcontrol.routes.dashboard import dashboard_bp
    from devcontrol.routes.veiculos import veiculos_bp
    from devcontrol.routes.entradas import entradas_bp
    from devcontrol.routes.saidas import saidas_bp
    from devcontrol.routes.pessoas import pessoas_bp

    # REGISTRA
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(entradas_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(saidas_bp)
    app.register_blueprint(pessoas_bp)


    return app
