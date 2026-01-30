from flask import Blueprint, render_template
from services.dashboard_service import get_dashboard_data

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    veiculos_patio, entradas_hoje, saidas_hoje = get_dashboard_data()

    return render_template(
        'dashboard/index.html',
        veiculos_patio=veiculos_patio,
        entradas_hoje=entradas_hoje,
        saidas_hoje=saidas_hoje
    )
