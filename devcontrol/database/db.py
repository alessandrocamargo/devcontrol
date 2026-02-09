import sqlite3

DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT UNIQUE NOT NULL,
            modelo TEXT NOT NULL,
            setor TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT,
            veiculo_id INTEGER,
            data_hora TEXT NOT NULL,
            tipo TEXT NOT NULL,
            km_entrada INTEGER,
            km_saida INTEGER
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registros_portaria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        documento TEXT,
        empresa TEXT,
        tipo TEXT NOT NULL, -- visitante | prestador
        data_entrada TEXT NOT NULL,
        data_saida TEXT,
        status TEXT NOT NULL -- dentro | saiu
    )
""")


    # Ensure migration: add missing columns if the table was created previously
    cursor.execute("PRAGMA table_info('registros_veiculos')")
    existing_cols = {row[1] for row in cursor.fetchall()}  # row[1] is column name

    # Add veiculo_id if missing (used as FK to veiculos.id)
    if 'veiculo_id' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE registros_veiculos ADD COLUMN veiculo_id INTEGER")
        except Exception:
            pass

    # Add km_entrada if missing
    if 'km_entrada' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE registros_veiculos ADD COLUMN km_entrada INTEGER")
        except Exception:
            pass

    # Add km_saida if missing
    if 'km_saida' not in existing_cols:
        try:
            cursor.execute("ALTER TABLE registros_veiculos ADD COLUMN km_saida INTEGER")
        except Exception:
            pass

    conn.commit()
    conn.close()
