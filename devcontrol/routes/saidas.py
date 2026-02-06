from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from devcontrol.database.db import get_db_connection

saidas_bp = Blueprint("saidas", __name__)

@saidas_bp.route("/saida", methods=["GET", "POST"])
def saida():
    conn = get_db_connection()

    if request.method == "POST":
        veiculo_id = request.form["veiculo_id"]
        km_saida = request.form["km_saida"]
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🔒 Regra de negócio: não sair sem entrada
        ultima_movimentacao = conn.execute(
            """
            SELECT tipo FROM registros_veiculos
            WHERE veiculo_id = ?
            ORDER BY data_hora DESC
            LIMIT 1
            """,
            (veiculo_id,)
        ).fetchone()

        if not ultima_movimentacao or ultima_movimentacao["tipo"] != "entrada":
            flash("Veículo não está no pátio para saída.", "error")
            conn.close()
            return redirect(url_for("saidas.saida"))

        conn.execute(
            """
            INSERT INTO registros_veiculos (veiculo_id, data_hora, tipo, km_saida)
            VALUES (?, ?, 'saida', ?)
            """,
            (veiculo_id, data_hora, km_saida)
        )
        conn.commit()
        conn.close()

        flash("Saída registrada com sucesso!", "success")
        return redirect(url_for("saidas.saida"))

    veiculos = conn.execute("SELECT * FROM veiculos").fetchall()
    conn.close()

    return render_template("saida.html", veiculos=veiculos)
