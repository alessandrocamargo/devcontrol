from flask import Blueprint, render_template, request,redirect, url_for
from services.portaria_service import registrar_entrada, registrar_saida
from database.db import get_db_connection

portaria_bp = Blueprint("portaria", __name__)

# Index Portaria
@portaria_bp.route("/portaria")
def index():
    conn = get_db_connection()
    registros = conn.execute("""SELECT * FROM  registros_portaria ORDEM BY data_entrada DESC""").fetchall()
    conn.close()
    return render_template("portaria/index.html", registros = registros)

# Registrar Entrada
@portaria_bp.route("/portaria/entrada", methods=["POST"])
def entrada():
    registrar_entrada(
        request.form["nome"],
        request.form["documento"],
        request.form["empresa"],
        request.form["tipo"]
    )
    return redirect(url_for("portaria.index"))

# Registrar Saida
@portaria_bp.route("/portaria/saida", methods=["POST"])
def saida(id):
    registrar_saida(id)
    return redirect(url_for("portaria.index"))