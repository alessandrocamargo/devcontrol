from flask import Flask, render_template, request, redirect,url_for, flash
import sqlite3
from database import get_db_connection, create_tables
from datetime import datetime


app = Flask(__name__)

app.secret_key = "devcontrol-secret"

def get_dashboard_data():
    conn = get_db_connection()

    total_veiculos = conn.execute(
        "SELECT COUNT(*) FROM veiculos"
    ).fetchone()[0]

    veiculos_dentro = conn.execute(
        "SELECT COUNT(*) FROM veiculos WHERE status = 'DENTRO'"
    ).fetchone()[0]

    veiculos_fora = conn.execute(
        "SELECT COUNT(*) FROM veiculos WHERE status = 'FORA'"
    ).fetchone()[0]

    conn.close()

    return total_veiculos, veiculos_dentro, veiculos_fora



@app.route('/')
def index():
    total_veiculos, veiculos_dentro, veiculos_fora = get_dashboard_data()
    return render_template(
        'index.html',
        total_veiculos=total_veiculos,
        veiculos_dentro=veiculos_dentro,
        veiculos_fora=veiculos_fora
    )


@app.route("/veiculos", methods=["GET", "POST"])
def veiculos():
    conn = get_db_connection()

    if request.method == "POST":
        placa = request.form["placa"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        setor = request.form["setor"]

        try:
            conn.execute(
                "INSERT INTO veiculos (placa, marca, modelo, setor) VALUES (?, ?, ?, ?)",
                (placa, marca, modelo, setor)
            )
            conn.commit()
            flash("Veículo cadastrado com sucesso!", "success")
        except sqlite3.IntegrityError:
            flash("Placa já cadastrada!", "error")
        finally:
            conn.close()

        return redirect(url_for("veiculos"))

    veiculos = conn.execute("SELECT * FROM veiculos").fetchall()
    conn.close()

    return render_template("veiculos.html", veiculos=veiculos)

@app.route('/entrada', methods=['GET', 'POST'])
def entrada():
    conn = get_db_connection()

    if request.method == 'POST':
        veiculo_id = request.form['veiculo_id']

        # registra movimentação
        conn.execute(
            "INSERT INTO movimentacoes (veiculo_id, tipo) VALUES (?, 'ENTRADA')",
            (veiculo_id,)
        )

        # atualiza status do veículo
        conn.execute(
            "UPDATE veiculos SET status = 'DENTRO' WHERE id = ?",
            (veiculo_id,)
        )

        conn.commit()
        conn.close()

        flash('Entrada registrada com sucesso!', 'success')
        return redirect(url_for('entrada'))

    # só veículos FORA podem entrar
    veiculos = conn.execute(
        "SELECT id, placa FROM veiculos WHERE status = 'FORA'"
    ).fetchall()

    conn.close()
    return render_template('entrada.html', veiculos=veiculos)

@app.route('/saida', methods=['GET', 'POST'])
def saida():
    conn = get_db_connection()

    if request.method == 'POST':
        veiculo_id = request.form['veiculo_id']

        conn.execute(
            "INSERT INTO movimentacoes (veiculo_id, tipo) VALUES (?, 'SAIDA')",
            (veiculo_id,)
        )

        conn.execute(
            "UPDATE veiculos SET status = 'FORA' WHERE id = ?",
            (veiculo_id,)
        )

        conn.commit()
        conn.close()

        flash('Saída registrada com sucesso!', 'success')
        return redirect(url_for('saida'))

    veiculos = conn.execute(
        "SELECT id, placa FROM veiculos WHERE status = 'DENTRO'"
    ).fetchall()
    conn.close()

    return render_template('saida.html', veiculos=veiculos)


if __name__ == "__main__":
    app.run(debug=True)