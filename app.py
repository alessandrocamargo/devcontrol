from flask import Flask, render_template, request, redirect,url_for, flash
import sqlite3
from database import get_db_connection, create_tables
from datetime import datetime


app = Flask(__name__)

app.secret_key = "devcontrol-secret"

create_tables()

def get_dashboard_data():
    conn = get_db_connection()

    total_entradas = conn.execute(
        "SELECT COUNT(*) FROM registros_veiculos WHERE tipo = 'entrada'"
    ).fetchone()[0]

    total_saidas = conn.execute(
        "SELECT COUNT(*) FROM registros_veiculos WHERE tipo = 'saida'"
    ).fetchone()[0]

    conn.close()

    veiculos_patio = total_entradas - total_saidas

    return total_entradas, total_saidas, veiculos_patio


@app.route('/')
def index():
    total_entradas, total_saidas, veiculos_patio = get_dashboard_data()
    return render_template(
        'index.html',
        total_entradas=total_entradas,
        total_saidas=total_saidas,
        veiculos_patio=veiculos_patio
    )

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


@app.route('/entrada', methods=['GET', 'POST'])
def entrada():
    if request.method == 'POST':
        placa = request.form['placa']
        modelo = request.form['modelo']
        setor = request.form['setor']
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO registros_veiculos(placa, modelo, setor, data_hora, tipo) VALUES(?, ?, ?, ?, ?)', (placa, modelo, setor, data_hora, 'entrada')
        )
        conn.commit()
        conn.close()

        return redirect(url_for('registros'))
    return render_template('entrada.html')

@app.route('/saida', methods=['GET', 'POST'])
def saida():
    if request.method == 'POST':
        placa = request.form['placa']
        modelo = request.form['modelo']
        setor = request.form['modelo']
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO registros_veiculos(placa, modelo, setor, data_hora, tipo) VALUES(?, ?, ?, ?, ?)', (placa, modelo, setor, data_hora, 'saida')
        )
        conn.commit()
        conn.close()

        return redirect(url_for('registros'))
    return render_template('saida.html')

@app.route('/registros')
def registros():
    conn = get_db_connection()
    registros = conn.execute(
        'SELECT *FROM registros_veiculos ORDER BY data_hora DESC'
    ).fetchall()
    conn.close()
    return render_template('registros.html', registros= registros)


if __name__ == "__main__":
    app.run(debug=True)