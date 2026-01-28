from flask import Flask, render_template, request, redirect,url_for
import sqlite3
from database import get_db_connection, create_table
from datetime import datetime


app = Flask(__name__)

create_table()

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
            'INSERT INTO registros_veiculos(placa, modelo, setor, data_hora, tipo) VALUES(?, ?, ?, ?, ?)', (placa, modelo, setor, data_hora, 'entrada')
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