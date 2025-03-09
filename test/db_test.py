import os
import sqlite3


def criar_banco_teste():
    conexao = sqlite3.connect(
        "track_jobs_test.db"
    )  # Banco de dados separado para testes
    cursor = conexao.cursor()

    # Criar tabela de empresas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            site TEXT,
            setor TEXT
        )
    """
    )

    # Criar tabela de vagas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'candidatar-se',
            descricao TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY (idEmpresa) REFERENCES empresas(id)
        )
    """
    )

    conexao.commit()
    conexao.close()


def criar_banco_teste_com_dados():
    conexao = sqlite3.connect(
        "track_jobs_test.db"
    )  # Banco de dados separado para testes
    cursor = conexao.cursor()

    # Criar tabela de empresas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            site TEXT,
            setor TEXT
        )
    """
    )

    # Criar tabela de vagas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'candidatar-se',
            data_aplicacao DATE DEFAULT CURRENT_DATE,
            descricao TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY (idEmpresa) REFERENCES empresas(id)
        )
    """
    )

    # Inserir algumas empresas para associar às vagas
    cursor.executemany(
        """
        INSERT OR IGNORE INTO empresas (nome, site, setor)
        VALUES (?, ?, ?)
    """,
        [
            ("Google", "https://careers.google.com", "Tecnologia"),
            ("Microsoft", "https://careers.microsoft.com", "Tecnologia"),
            ("Amazon", "https://www.amazon.jobs", "E-commerce"),
        ],
    )

    # Pegar IDs das empresas recém-criadas
    cursor.execute("SELECT id FROM empresas WHERE nome = 'Google'")
    google_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM empresas WHERE nome = 'Microsoft'")
    microsoft_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM empresas WHERE nome = 'Amazon'")
    amazon_id = cursor.fetchone()[0]

    # Inserir 10 vagas de teste
    vagas_teste = [
        (
            "Desenvolvedor Backend",
            "https://jobs.example.com/1",
            "candidatar-se",
            "Trabalhar com APIs e microsserviços",
            google_id,
        ),
        (
            "Engenheiro de Software",
            "https://jobs.example.com/2",
            "entrevista",
            "Desenvolvimento fullstack",
            microsoft_id,
        ),
        (
            "Analista de Dados",
            "https://jobs.example.com/3",
            "candidatar-se",
            "Analisar grandes volumes de dados",
            amazon_id,
        ),
        (
            "Desenvolvedor Mobile",
            "https://jobs.example.com/4",
            "candidatar-se",
            "Apps Android e iOS",
            google_id,
        ),
        (
            "DevOps Engineer",
            "https://jobs.example.com/5",
            "teste técnico",
            "Automação e CI/CD",
            microsoft_id,
        ),
        (
            "Product Manager",
            "https://jobs.example.com/6",
            "candidatar-se",
            "Gerenciar backlog e roadmap",
            amazon_id,
        ),
        (
            "QA Engineer",
            "https://jobs.example.com/7",
            "candidatar-se",
            "Testes automatizados",
            google_id,
        ),
        (
            "Data Scientist",
            "https://jobs.example.com/8",
            "entrevista",
            "Modelagem de dados avançada",
            microsoft_id,
        ),
        (
            "Cloud Engineer",
            "https://jobs.example.com/9",
            "candidatar-se",
            "Arquitetura de nuvem",
            amazon_id,
        ),
        (
            "Software Architect",
            "https://jobs.example.com/10",
            "candidatar-se",
            "Definir padrões e arquitetura",
            google_id,
        ),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO vagas (nome, link, status, descricao, idEmpresa)
        VALUES (?, ?, ?, ?, ?)
    """,
        vagas_teste,
    )

    conexao.commit()
    conexao.close()


def remove_banco_teste():
    if os.path.exists("track_jobs_test.db"):
        os.remove("track_jobs_test.db")
