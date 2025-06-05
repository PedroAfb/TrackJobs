import sqlite3
from unittest.mock import Mock

import pytest

from trackJobs.exceptions import CampoDuplicadoException
from trackJobs.exceptions import ErroCandidaturaException
from trackJobs.model.repositories.SQLite.base_repository import BaseSQLiteRepository


class TestBaseSQLiteRepository:
    """Testes unitários para o BaseSQLiteRepository"""

    def setup_method(self):
        """Setup para cada teste - cria mock para o banco de dados"""
        self.db_mock = Mock()
        self.cursor_mock = Mock()
        self.conexao_mock = Mock()
        self.db_mock.cursor = self.cursor_mock
        self.db_mock.conexao = self.conexao_mock

        self.base_repository = BaseSQLiteRepository(self.db_mock)

    def test_transaction_sucesso(self):
        """Testa transação com sucesso"""
        # Act
        with self.base_repository.transaction() as cursor:
            cursor.execute("SELECT 1")

        # Assert
        self.conexao_mock.commit.assert_called_once()
        self.conexao_mock.rollback.assert_not_called()

    def test_transaction_erro_integridade(self):
        """Testa transação com erro de integridade (violação de chave única)"""
        # Arrange
        self.cursor_mock.execute.side_effect = sqlite3.IntegrityError(
            "UNIQUE constraint failed: vagas.link"
        )

        # Act & Assert
        with pytest.raises(CampoDuplicadoException) as excinfo:
            with self.base_repository.transaction() as cursor:
                cursor.execute("INSERT INTO vagas (link) VALUES ('test')")

        assert "O campo 'vagas.link'" in str(excinfo.value)
        self.conexao_mock.rollback.assert_called_once()
        self.conexao_mock.commit.assert_not_called()

    def test_transaction_erro_database(self):
        """Testa transação com erro de banco de dados"""
        # Arrange
        self.cursor_mock.execute.side_effect = sqlite3.DatabaseError(
            "Erro no banco de dados"
        )

        # Act & Assert
        with pytest.raises(ErroCandidaturaException) as excinfo:
            with self.base_repository.transaction() as cursor:
                cursor.execute("SELECT * FROM tabela_inexistente")

        assert "Erro no banco de dados" in str(excinfo.value)
        self.conexao_mock.rollback.assert_called_once()
        self.conexao_mock.commit.assert_not_called()

    def test_transaction_erro_generico(self):
        """Testa transação com erro genérico"""
        # Arrange
        self.cursor_mock.execute.side_effect = Exception("Erro genérico")

        # Act & Assert
        with pytest.raises(Exception) as excinfo:
            with self.base_repository.transaction() as cursor:
                cursor.execute("SELECT 1")

        assert "Erro genérico" in str(excinfo.value)
        self.conexao_mock.rollback.assert_called_once()
        self.conexao_mock.commit.assert_not_called()
