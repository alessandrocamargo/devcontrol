from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

from database import get_db_connection, create_tables
from routes.dashboard import get_dashboard_data

app = Flask(__name__)
app.secret_key = "devcontrol-secret"

# Cria as tabelas ao iniciar o app
create_tables()


# ======================
# DASHBOARD
# ======================
@app.route("/")
def index():
    veiculos_dentro, entradas_hoje, saidas_hoje, total_veiculos = get_dashboard_data()

    return render_template(
        "index.html",
        veiculos_dentro=veiculos_dentro,
        entradas_hoje=entradas_hoje,
        saidas_hoje=saidas_hoje,
        total_veiculos=total_veiculos
    )


# ======================
# VEÍCULOS
# ======================
@app.route("/veiculos", methods=["GET", "POST"])
def veiculos():
    conn = get_db_connection()

    if request.method == "POST":
        placa = request.form["placa"]
        modelo = request.form["modelo"]
        setor = request.form["setor"]

        try:
            conn.execute(
                "INSERT INTO veiculos (placa, modelo, setor) VALUES (?, ?, ?)",
                (placa, modelo, setor)
            )
            conn.commit()
            flash("Veículo cadastrado com sucesso!", "success")
        except Exception:
            flash("Placa já cadastrada!", "error")
        finally:
            conn.close()

        return redirect(url_for("veiculos"))

    veiculos = conn.execute("SELECT * FROM veiculos").fetchall()
    conn.close()

    return render_template("veiculos.html", veiculos=veiculos)


# ======================
# ENTRADA
# ======================
@app.route("/entrada", methods=["GET", "POST"])
def entrada():
    conn = get_db_connection()

    if request.method == "POST":
        veiculo_id = request.form["veiculo_id"]
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            """
            INSERT INTO registros_veiculos (veiculo_id, data_hora, tipo)
            VALUES (?, ?, 'entrada')
            """,
            (veiculo_id, data_hora)
        )
        conn.commit()
        conn.close()

        flash("Entrada registrada com sucesso!", "success")
        return redirect(url_for("entrada"))

    veiculos = conn.execute("SELECT * FROM veiculos").fetchall()
    conn.close()

    return render_template("entrada.html", veiculos=veiculos)


# ======================
# SAÍDA
# ======================
@app.route("/saida", methods=["GET", "POST"])
def saida():
    conn = get_db_connection()

    if request.method == "POST":
        veiculo_id = request.form["veiculo_id"]
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute(
            """
            INSERT INTO registros_veiculos (veiculo_id, data_hora, tipo)
            VALUES (?, ?, 'saida')
            """,
            (veiculo_id, data_hora)
        )
        conn.commit()
        conn.close()

        flash("Saída registrada com sucesso!", "success")
        return redirect(url_for("saida"))

    veiculos = conn.execute("SELECT * FROM veiculos").fetchall()
    conn.close()

    return render_template("saida.html", veiculos=veiculos)


# ======================
# REGISTROS
# ======================
@app.route("/registros")
def registros():
    conn = get_db_connection()

    registros = conn.execute(
        """
        SELECT r.id, v.placa, v.modelo, v.setor, r.data_hora, r.tipo
        FROM registros_veiculos r
        JOIN veiculos v ON v.id = r.veiculo_id
        ORDER BY r.data_hora DESC
        """
    ).fetchall()

    conn.close()

    return render_template("registros.html", registros=registros)


if __name__ == "__main__":
    app.run(debug=True)
