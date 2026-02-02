from database.db import get_db_connection
from datetime import date

def get_dashboard_data():
    conn = get_db_connection()
    hoje = date.today().strftime("%Y-%m-%d")

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

    # Veículos no pátio
    veiculos_dentro = conn.execute("""
    SELECT COUNT(*)
    FROM veiculos v
    WHERE NOT EXISTS (
        SELECT 1
        FROM registros_veiculos r2
        WHERE r2.veiculo_id = v.id
          AND r2.tipo = 'saida'
          AND r2.data_hora > (
              SELECT r1.data_hora
              FROM registros_veiculos r1
              WHERE r1.veiculo_id = v.id
                AND r1.tipo = 'entrada'
              ORDER BY r1.data_hora DESC
              LIMIT 1
          )
    )
""").fetchone()[0]


    # KM rodados hoje
    km_rodados = conn.execute("""
    SELECT COALESCE(SUM(r2.km_saida - r1.km_entrada), 0)
    FROM registros_veiculos r1
    JOIN registros_veiculos r2
      ON r1.veiculo_id = r2.veiculo_id
    WHERE r1.tipo = 'entrada'
      AND r2.tipo = 'saida'
      AND date(r2.data_hora) = ?
""", (hoje,)).fetchone()[0]


    conn.close()

    return veiculos_dentro, entradas_hoje, saidas_hoje, km_rodados
