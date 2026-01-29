from flask import Flask
from routes.dashboard import dashboard_bp
from routes.veiculos import veiculos_bp
from routes.entradas import entradas_bp
from routes.saidas import saidas_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "devcontrol-secret"

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(entradas_bp)
    app.register_blueprint(saidas_bp)

    return app

app = create_app()
