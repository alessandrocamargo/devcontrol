from database import get_db_connection

def get_dashboard_data():
    conn = get_db_connection()

    total_veiculos = conn.execute(
        "SELECT COUNT(*) FROM veiculos"
    ).fetchone()[0]

    entradas_hoje = conn.execute(
        """
        SELECT COUNT(*)
        FROM registros_veiculos
        WHERE tipo = 'entrada'
        AND DATE(data_hora) = DATE('now', 'localtime')
        """
    ).fetchone()[0]

    saidas_hoje = conn.execute(
        """
        SELECT COUNT(*)
        FROM registros_veiculos
        WHERE tipo = 'saida'
        AND DATE(data_hora) = DATE('now', 'localtime')
        """
    ).fetchone()[0]

    veiculos_dentro = conn.execute(
        """
        SELECT COUNT(*)
        FROM veiculos v
        WHERE (
            SELECT r.tipo
            FROM registros_veiculos r
            WHERE r.veiculo_id = v.id
            ORDER BY r.data_hora DESC
            LIMIT 1
        ) = 'entrada'
        """
    ).fetchone()[0]

    conn.close()

    return veiculos_dentro, entradas_hoje, saidas_hoje, total_veiculos
