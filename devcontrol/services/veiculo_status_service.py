from devcontrol.database.db import get_db_connection

def listar_veiculos_com_status():
    conn = get_db_connection()

    veiculos = conn.execute("""
        SELECT 
            v.id,
            v.placa,
            v.modelo,
            v.setor,
            (
                SELECT r.tipo
                FROM registros_veiculos r
                WHERE r.veiculo_id = v.id
                ORDER BY r.data_hora DESC
                LIMIT 1
            ) AS ultimo_status
        FROM veiculos v
        ORDER BY v.placa
    """).fetchall()

    conn.close()
    return veiculos
