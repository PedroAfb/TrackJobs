from unittest.mock import Mock

import pytest

from trackJobs.exceptions import DataInvalidaException
from trackJobs.exceptions import NomeVazioException
from trackJobs.exceptions import StatusInvalidoException
from trackJobs.exceptions import URLInvalidaException
from trackJobs.exceptions import URLJaCadastradaException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.services.validadores.vaga_validador_service import (
    VagaValidadorService,
)


class TestVagaValidadorService:
    """Testes unitários para o VagaValidadorService"""

    def setup_method(self):
        """Setup para cada teste - cria mock para o repository"""
        self.vaga_repository_mock = Mock()
        self.validador = VagaValidadorService(self.vaga_repository_mock)

    def test_valida_nome_valido(self):
        """Testa validação de nome válido"""
        # Act
        resultado = self.validador.valida_nome("Desenvolvedor Python")

        # Assert
        assert resultado is True

    def test_valida_nome_vazio(self):
        """Testa validação de nome vazio"""
        # Act & Assert
        with pytest.raises(NomeVazioException):
            self.validador.valida_nome("")

    def test_valida_link_valido(self):
        """Testa validação de link válido"""
        # Arrange
        self.vaga_repository_mock.buscar_vaga_por_link.return_value = None

        # Act
        resultado = self.validador.valida_link("https://example.com/vaga")

        # Assert
        assert resultado is True
        self.vaga_repository_mock.buscar_vaga_por_link.assert_called_once_with(
            "https://example.com/vaga"
        )

    def test_valida_link_vazio(self):
        """Testa validação de link vazio"""
        # Act & Assert
        with pytest.raises(URLInvalidaException):
            self.validador.valida_link("")

        self.vaga_repository_mock.buscar_vaga_por_link.assert_not_called()

    def test_valida_link_invalido(self):
        """Testa validação de link inválido"""
        # Act & Assert
        with pytest.raises(URLInvalidaException):
            self.validador.valida_link("example-vaga")

        self.vaga_repository_mock.buscar_vaga_por_link.assert_not_called()

    def test_valida_link_duplicado(self):
        """Testa validação de link duplicado"""
        # Arrange
        vaga_mock = Vaga(
            id=1,
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
        )
        self.vaga_repository_mock.buscar_vaga_por_link.return_value = vaga_mock

        # Act & Assert
        with pytest.raises(URLJaCadastradaException):
            self.validador.valida_link("https://example.com/vaga")

        self.vaga_repository_mock.buscar_vaga_por_link.assert_called_once_with(
            "https://example.com/vaga"
        )

    def test_valida_status_valido(self):
        """Testa validação de status válido"""
        # Act & Assert
        status_validos = [
            "candidatar-se",
            "em análise",
            "entrevista",
            "rejeitado",
            "aceito",
        ]

        for status in status_validos:
            resultado = self.validador.valida_status(status)
            assert resultado is True

    def test_valida_status_invalido(self):
        """Testa validação de status inválido"""
        # Act & Assert
        with pytest.raises(StatusInvalidoException):
            self.validador.valida_status("status_invalido")

    def test_valida_status_case_insensitive(self):
        """Testa validação de status com case insensitive"""
        # Act
        resultado = self.validador.valida_status("CANDIDATAR-SE")

        # Assert
        assert resultado is True

    def test_valida_data_aplicacao_valida(self):
        """Testa validação de data de aplicação válida"""
        # Act
        resultado = self.validador.valida_data_aplicacao("2025-06-01")

        # Assert
        assert resultado is True

    def test_valida_data_aplicacao_vazia(self):
        """Testa validação de data de aplicação vazia (opcional)"""
        # Act
        resultado = self.validador.valida_data_aplicacao("")

        # Assert
        assert resultado is True

    def test_valida_data_aplicacao_invalida(self):
        """Testa validação de data de aplicação inválida"""
        # Act & Assert
        with pytest.raises(DataInvalidaException):
            self.validador.valida_data_aplicacao("01/06/2025")

        with pytest.raises(DataInvalidaException):
            self.validador.valida_data_aplicacao("texto_invalido")
