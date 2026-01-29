from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
from database.db import get_db_connection

veiculos_bp = Blueprint("veiculos", __name__, url_prefix="/veiculos")


@veiculos_bp.route("/", methods=["GET", "POST"])
def veiculos():
    conn = get_db_connection()

    if request.method == "POST":
        placa = request.form.get("placa")
        modelo = request.form.get("modelo")
        setor = request.form.get("setor")

        if not placa or not modelo or not setor:
            flash("Preencha todos os campos.", "error")
            conn.close()
            return redirect(url_for("veiculos.veiculos"))

        try:
            conn.execute(
                """
                INSERT INTO veiculos (placa, modelo, setor)
                VALUES (?, ?, ?)
                """,
                (placa.upper(), modelo, setor)
            )
            conn.commit()
            flash("Veículo cadastrado com sucesso!", "success")

        except sqlite3.IntegrityError:
            flash("Já existe um veículo cadastrado com essa placa.", "error")

        except Exception as e:
            flash(f"Erro ao cadastrar veículo: {e}", "error")

        finally:
            conn.close()

        return redirect(url_for("veiculos.veiculos"))

    veiculos = conn.execute(
        "SELECT * FROM veiculos ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("veiculos.html", veiculos=veiculos)
