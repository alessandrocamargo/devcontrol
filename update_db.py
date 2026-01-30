import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE registros_veiculos
ADD COLUMN km_saida INTEGER
""")

conn.commit()
conn.close()

print("Coluna km_entrada adicionada com sucesso!")
