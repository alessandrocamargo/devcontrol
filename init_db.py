import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database.db")
    return conn

conn = get_db_connection()  # 👈 CHAMADA da função
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT UNIQUE NOT NULL,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    setor TEXT,
    status TEXT NOT NULL DEFAULT 'FORA',
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    veiculo_id INTEGER NOT NULL,
    tipo TEXT CHECK (tipo IN ('ENTRADA', 'SAIDA')) NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
);
""")

conn.commit()
conn.close()
