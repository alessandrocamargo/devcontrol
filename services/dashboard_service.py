from devcontrol.db import get_db_connection
from datetime import date

def get_dashboard_data():
    conn = get_db_connection()

    veiculos_dentro = conn.execute("""
        SELECT COUNT(*) FROM registros_veiculos r1
        WHERE tipo = 'entrada'
        AND NOT EXISTS (
            SELECT 1 FROM registros_veiculos r2
            WHERE r2.placa = r1.placa AND r2.tipo = 'saida'
            AND r2.data_hora > r1.data_hora
        )
    """).fetchone()[0]

    hoje = date.today().isoformat()

    entradas_hoje = conn.execute(
        "SELECT COUNT(*) FROM registros_veiculos WHERE tipo='entrada' AND data_hora LIKE ?",
        (f"{hoje}%",)
    ).fetchone()[0]

    saidas_hoje = conn.execute(
        "SELECT COUNT(*) FROM registros_veiculos WHERE tipo='saida' AND data_hora LIKE ?",
        (f"{hoje}%",)
    ).fetchone()[0]

    conn.close()

    return veiculos_dentro, entradas_hoje, saidas_hoje
