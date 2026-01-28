import sqlite3

DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de veículos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT UNIQUE NOT NULL,
            modelo TEXT NOT NULL,
            setor TEXT NOT NULL
        )
    """)

    # Tabela de registros (entrada/saída)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            tipo TEXT NOT NULL,
            FOREIGN KEY (veiculo_id) REFERENCES veiculos (id)
        )
    """)

    conn.commit()
    conn.close()
