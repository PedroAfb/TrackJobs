import sqlite3

import pytest

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.job_model import JobModel


# Fixtures para teste de integração
@pytest.fixture
def setup_test_db():
    """Configura banco de dados de teste"""
    db_path = "track_jobs_test.db"

    # Criar banco de teste
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar tabelas
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS empresas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            site TEXT,
            setor TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vagas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            status TEXT,
            descriçao TEXT,
            data_aplicaçao TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY (idEmpresa) REFERENCES empresas(id)
        )
    """
    )

    conn.commit()
    conn.close()

    yield db_path

    # Limpar após os testes
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS vagas")
    cursor.execute("DROP TABLE IF EXISTS empresas")
    conn.commit()
    conn.close()


class TestIntegracaoCadastro:
    """Testes de integração para o fluxo completo de cadastro"""

    def test_cadastro_sem_empresa(self, setup_test_db):
        """Testa cadastro de vaga sem empresa (integração)"""
        # Arrange
        db_path = setup_test_db
        model = JobModel(db_path=db_path)
        controller = JobController(model)

        dados_vaga = {
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "candidatar-se",
            "descriçao": "Vaga para desenvolvedor Python",
            "data_aplicaçao": "2025-06-01",
        }

        # Act
        resultado = controller.cadastra_candidatura(dados_vaga)

        # Assert
        assert "Cadastro da vaga realizado com sucesso" in resultado

        # Verificar se foi realmente salvo no banco
        db = BancoDeDados(db_path)
        cursor = db.cursor
        cursor.execute(
            "SELECT COUNT(*) FROM vagas WHERE link = ?", ("https://example.com/vaga",)
        )
        count = cursor.fetchone()[0]
        assert count == 1

    def test_cadastro_com_empresa_nova(self, setup_test_db):
        """Testa cadastro de vaga com nova empresa (integração)"""
        # Arrange
        db_path = setup_test_db
        model = JobModel(db_path=db_path)
        controller = JobController(model)

        dados_vaga = {
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "candidatar-se",
            "descriçao": "Vaga para desenvolvedor Python",
            "data_aplicaçao": "2025-06-01",
            "nome_empresa": "TechCorp",
            "site_empresa": "https://techcorp.com",
            "setor_empresa": "Tecnologia",
        }

        # Act
        resultado = controller.cadastra_candidatura(dados_vaga)

        # Assert
        assert "Cadastro da vaga realizado com sucesso" in resultado

        # Verificar empresa
        db = BancoDeDados(db_path)
        cursor = db.cursor
        cursor.execute("SELECT COUNT(*) FROM empresas WHERE nome = ?", ("techcorp",))
        count = cursor.fetchone()[0]
        assert count == 1

        # Verificar vaga e sua relação com empresa
        cursor.execute(
            """
            SELECT v.nome, e.nome
            FROM vagas v
            JOIN empresas e ON v.idEmpresa = e.id
            WHERE v.link = ?
        """,
            ("https://example.com/vaga",),
        )

        resultado_db = cursor.fetchone()
        assert resultado_db[0] == "Desenvolvedor Python".lower()
        assert resultado_db[1] == "TechCorp".lower()

    def test_cadastro_com_empresa_existente(self, setup_test_db):
        """Testa cadastro de vaga com empresa existente (integração)"""
        # Arrange
        db_path = setup_test_db
        model = JobModel(db_path=db_path)
        controller = JobController(model)

        # Primeiro cadastrar a empresa
        db = BancoDeDados(db_path)
        cursor = db.cursor
        cursor.execute(
            "INSERT INTO empresas (nome, site, setor) VALUES (?, ?, ?)",
            ("techcorp", "https://techcorp.com", "Tecnologia"),
        )
        db.conexao.commit()

        dados_vaga = {
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "candidatar-se",
            "descriçao": "Vaga para desenvolvedor Python",
            "data_aplicaçao": "2025-06-01",
            "nome_empresa": "TechCorp",
        }

        # Act
        resultado = controller.cadastra_candidatura(dados_vaga)

        # Assert
        assert "Cadastro da vaga realizado com sucesso" in resultado

        # Verificar que não criou uma nova empresa
        cursor.execute("SELECT COUNT(*) FROM empresas")
        count = cursor.fetchone()[0]
        assert count == 1

        # Verificar relação vaga-empresa
        cursor.execute(
            """
            SELECT v.nome, e.nome
            FROM vagas v
            JOIN empresas e ON v.idEmpresa = e.id
            WHERE v.link = ?
        """,
            ("https://example.com/vaga",),
        )

        resultado_db = cursor.fetchone()
        assert resultado_db[0] == "Desenvolvedor Python".lower()
        assert resultado_db[1] == "TechCorp".lower()

    def test_cadastro_link_duplicado(self, setup_test_db):
        """Testa tentativa de cadastro com link duplicado (integração)"""
        # Arrange
        db_path = setup_test_db
        model = JobModel(db_path=db_path)
        controller = JobController(model)

        # Primeiro cadastro
        dados_vaga1 = {
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "candidatar-se",
        }
        controller.cadastra_candidatura(dados_vaga1)

        # Segundo cadastro com mesmo link
        dados_vaga2 = {
            "nome": "Programador Python",
            "link": "https://example.com/vaga",  # Mesmo link
            "status": "candidatar-se",
        }

        # Act & Assert
        with pytest.raises(TrackJobsException) as excinfo:
            controller.cadastra_candidatura(dados_vaga2)

        assert (
            "já está cadastrado" in str(excinfo.value).lower()
            or "duplicado" in str(excinfo.value).lower()
        )

        # Verificar que só existe uma vaga no banco
        db = BancoDeDados(db_path)
        cursor = db.cursor
        cursor.execute("SELECT COUNT(*) FROM vagas")
        count = cursor.fetchone()[0]
        assert count == 1
