from flask import Blueprint, render_template
from devcontrol.services.dashboard_service import get_dashboard_data

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    veiculos_dentro, entradas_hoje, saidas_hoje, km_rodados = get_dashboard_data()

    return render_template(
        "dashboard/index.html",
        veiculos_dentro=veiculos_dentro,
        entradas_hoje=entradas_hoje,
        saidas_hoje=saidas_hoje,
        km_rodados=km_rodados
    )
