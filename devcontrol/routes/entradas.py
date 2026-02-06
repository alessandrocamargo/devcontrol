from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from devcontrol.database.db import get_db_connection


entradas_bp = Blueprint("entradas", __name__)

@entradas_bp.route("/entrada", methods=["GET", "POST"])
def entrada():
    conn = get_db_connection()

    if request.method == "POST":
        veiculo_id = request.form["veiculo_id"]
        km_entrada = request.form["km_entrada"]
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

        conn.execute(
            """
            INSERT INTO registros_veiculos (veiculo_id, data_hora, tipo, km_entrada)
            VALUES (?, ?, 'entrada',?)
            """,
            (veiculo_id, data_hora, km_entrada)
        )
        conn.commit()
        conn.close()

        flash("Entrada registrada com sucesso!", "success")
        return redirect(url_for("entradas.entrada"))

    veiculos = conn.execute("SELECT * FROM veiculos").fetchall()
    conn.close()

    return render_template("entrada.html", veiculos=veiculos)
