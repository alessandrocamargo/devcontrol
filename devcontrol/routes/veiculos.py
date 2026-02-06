import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash

from devcontrol.database.db import get_db_connection
from devcontrol.services.veiculo_status_service import listar_veiculos_com_status

veiculos_bp = Blueprint(
    "veiculos",
    __name__,
    url_prefix="/veiculos"
)

@veiculos_bp.route("/menu",methods=["GET"])
def menu_veiculos():
    return render_template("veiculos/menu.html")

# ==============================
# LISTAR VEÍCULOS + STATUS
# ==============================
@veiculos_bp.route("/", methods=["GET"])
def listar_veiculos():
    veiculos = listar_veiculos_com_status()
    return render_template("veiculos/listar.html", veiculos=veiculos)


# ==============================
# FORMULÁRIO DE CADASTRO
# ==============================
@veiculos_bp.route("/novo", methods=["GET"])
def novo_veiculo():
    return render_template("veiculos/novo.html")


# ==============================
# SALVAR VEÍCULO
# ==============================
@veiculos_bp.route("/", methods=["POST"])
def criar_veiculo():
    placa = request.form["placa"]
    modelo = request.form["modelo"]
    setor = request.form["setor"]

    conn = get_db_connection()

    try:
        conn.execute(
            """
            INSERT INTO veiculos (placa, modelo, setor)
            VALUES (?, ?, ?)
            """,
            (placa, modelo, setor)
        )
        conn.commit()
        flash("Veículo cadastrado com sucesso!", "success")

    except sqlite3.IntegrityError:
        # erro REAL de placa duplicada
        flash("Já existe um veículo cadastrado com essa placa.", "warning")

    except Exception as e:
        # erro inesperado (não mascarar!)
        flash(f"Erro ao cadastrar veículo: {e}", "danger")

    finally:
        conn.close()

    return redirect(url_for("veiculos.novo_veiculo"))
