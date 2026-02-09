from database.db import get_db_connection
from datetime import datetime

def registrar_entrada(nome, documento, empresa, tipo):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO registros_portaria(nome, documento, empresa, tipo, data_entrada, status)
        VALUES (?, ?, ?, ?, ?, 'dentro')
    """,(
        nome, documento, empresa, tipo, datetime.now().strftime(" %d - %m - %Y %H : %M : %S ")
    ))

    conn.commit()
    conn.close()

    def registrar_saida(registro_id):
        conn = get_db_connection()
        conn.execute("""
            UPDATE registros_portaria SET data_saida = ?, status = 'saiu' WHERE id = ?
        """, (
            datetime.now().strftime(" %d - %m - %Y %H : %M : %S "),
            registro_id
        ))

        conn.commit()
        conn.close()