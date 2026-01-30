from database.db import get_db_connection

def get_dashboard_data():
    conn = get_db_connection()

    entradas_hoje = conn.execute("""
        SELECT COUNT(*) 
        FROM registros_veiculos 
        WHERE tipo = 'entrada'
        AND DATE(data_hora) = DATE('now')
    """).fetchone()[0]

    saidas_hoje = conn.execute("""
        SELECT COUNT(*) 
        FROM registros_veiculos 
        WHERE tipo = 'saida'
        AND DATE(data_hora) = DATE('now')
    """).fetchone()[0]

    total_entradas = conn.execute("""
        SELECT COUNT(*) 
        FROM registros_veiculos 
        WHERE tipo = 'entrada'
    """).fetchone()[0]

    total_saidas = conn.execute("""
        SELECT COUNT(*) 
        FROM registros_veiculos 
        WHERE tipo = 'saida'
    """).fetchone()[0]

    conn.close()

    veiculos_patio = total_entradas - total_saidas

    return veiculos_patio, entradas_hoje, saidas_hoje
