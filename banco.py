import sqlite3

conn = sqlite3.connect('pets.db')
cursor = conn.cursor()

# Criação da tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pet (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        raca TEXT,
        porte TEXT,
        status TEXT
    )
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
