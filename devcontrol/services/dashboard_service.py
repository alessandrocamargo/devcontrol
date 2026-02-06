from datetime import date
from devcontrol.database.db import get_db_connection

def get_dashboard_data():
    conn = get_db_connection()
    hoje = date.today().isoformat()

    # Veículos atualmente no pátio
    veiculos_dentro = conn.execute("""
        SELECT COUNT(DISTINCT r1.veiculo_id)
        FROM registros_veiculos r1
        WHERE r1.tipo = 'entrada'
        AND NOT EXISTS (
            SELECT 1 FROM registros_veiculos r2
            WHERE r2.veiculo_id = r1.veiculo_id
            AND r2.tipo = 'saida'
            AND r2.data_hora > r1.data_hora
        )
    """).fetchone()[0]

    # Entradas hoje
    entradas_hoje = conn.execute("""
        SELECT COUNT(*)
        FROM registros_veiculos
        WHERE tipo = 'entrada'
        AND date(data_hora) = ?
    """, (hoje,)).fetchone()[0]

    # Saídas hoje
    saidas_hoje = conn.execute("""
        SELECT COUNT(*)
        FROM registros_veiculos
        WHERE tipo = 'saida'
        AND date(data_hora) = ?
    """, (hoje,)).fetchone()[0]

    # KM rodados hoje
    km_rodados = conn.execute("""
        SELECT COALESCE(SUM(km_saida - km_entrada), 0)
        FROM registros_veiculos
        WHERE tipo = 'saida'
        AND date(data_hora) = ?
    """, (hoje,)).fetchone()[0]

    conn.close()

    return veiculos_dentro, entradas_hoje, saidas_hoje, km_rodados
