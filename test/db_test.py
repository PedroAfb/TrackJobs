import sqlite3
import os

def criar_banco_teste():
    conexao = sqlite3.connect("track_jobs_test.db")  # Banco de dados separado para testes
    cursor = conexao.cursor()

    # Criar tabela de empresas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            site TEXT,
            setor TEXT
        )
    """)

    # Criar tabela de vagas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'candidatar-se',
            descricao TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY (idEmpresa) REFERENCES empresas(id)
        )
    """)

    conexao.commit()
    conexao.close()


def remove_banco_teste():
    if os.path.exists("track_jobs_test.db"):
        os.remove("track_jobs_test.db")
