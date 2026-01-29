from database.db import get_db_connection
from datetime import date

def get_dashboard_data():
    conn = get_db_connection()

    # Veículos atualmente no pátio
    veiculos_dentro = conn.execute("""
        SELECT 
            COUNT(*) 
        FROM registros_veiculos
        WHERE tipo = 'entrada'
    """).fetchone()[0] - conn.execute("""
        SELECT 
            COUNT(*) 
        FROM registros_veiculos
        WHERE tipo = 'saida'
    """).fetchone()[0]

    hoje = date.today().strftime("%Y-%m-%d")

    entradas_hoje = conn.execute("""
        SELECT COUNT(*) 
        FROM registros_veiculos
        WHERE tipo = 'entrada'
          AND DATE(data_hora) = ?
    """, (hoje,)).fetchone()[0]

    saidas_hoje = conn.execute("""
        SELECT COUNT(*) 
        FROM registros_veiculos
        WHERE tipo = 'saida'
          AND DATE(data_hora) = ?
    """, (hoje,)).fetchone()[0]

    conn.close()

    return veiculos_dentro, entradas_hoje, saidas_hoje
