from unittest.mock import Mock

import pytest

from trackJobs.exceptions import DataInvalidaException
from trackJobs.exceptions import NomeVazioException
from trackJobs.exceptions import URLInvalidaException
from trackJobs.model.services.validadores.validador_service import ValidadorService


class TestValidadorService:
    """Testes unitários para o ValidadorService"""

    def setup_method(self):
        """Setup para cada teste - cria mocks para os validadores específicos"""
        self.empresa_validador_mock = Mock()
        self.vaga_validador_mock = Mock()
        self.validador_service = ValidadorService(
            self.empresa_validador_mock, self.vaga_validador_mock
        )

        # Configurar comportamento padrão (sucesso) para os validadores mockados
        self.empresa_validador_mock.valida_nome_empresa.return_value = True
        self.empresa_validador_mock.valida_link_empresa.return_value = True
        self.vaga_validador_mock.valida_nome.return_value = True
        self.vaga_validador_mock.valida_link.return_value = True
        self.vaga_validador_mock.valida_status.return_value = True
        self.vaga_validador_mock.valida_data_aplicacao.return_value = True

    def test_validacao_nome_vaga(self):
        """Testa validação de nome de vaga"""
        # Act
        self.validador_service.VALIDADORES["nome"]("Desenvolvedor Python")

        # Assert
        self.vaga_validador_mock.valida_nome.assert_called_once_with(
            "Desenvolvedor Python"
        )

    def test_validacao_nome_vaga_erro(self):
        """Testa validação de nome de vaga com erro"""
        # Arrange
        self.vaga_validador_mock.valida_nome.side_effect = NomeVazioException()

        # Act & Assert
        with pytest.raises(NomeVazioException):
            self.validador_service.VALIDADORES["nome"]("")

        self.vaga_validador_mock.valida_nome.assert_called_once_with("")

    def test_validacao_link_vaga(self):
        """Testa validação de link de vaga"""
        # Act
        self.validador_service.VALIDADORES["link"]("https://example.com/vaga")

        # Assert
        self.vaga_validador_mock.valida_link.assert_called_once_with(
            "https://example.com/vaga"
        )

    def test_validacao_link_vaga_erro(self):
        """Testa validação de link de vaga com erro"""
        # Arrange
        self.vaga_validador_mock.valida_link.side_effect = URLInvalidaException()

        # Act & Assert
        with pytest.raises(URLInvalidaException):
            self.validador_service.VALIDADORES["link"]("link-invalido")

        self.vaga_validador_mock.valida_link.assert_called_once_with("link-invalido")

    def test_validacao_status_vaga(self):
        """Testa validação de status de vaga"""
        # Act
        self.validador_service.VALIDADORES["status"]("candidatar-se")

        # Assert
        self.vaga_validador_mock.valida_status.assert_called_once_with("candidatar-se")

    def test_validacao_descricao_vaga(self):
        """Testa validação de descrição de vaga (sempre válida)"""
        # Act
        resultado = self.validador_service.VALIDADORES["descriçao"](
            "Descrição qualquer"
        )

        # Assert
        assert resultado is True

    def test_validacao_data_aplicacao(self):
        """Testa validação de data de aplicação"""
        # Act
        self.validador_service.VALIDADORES["data_aplicaçao"]("2025-06-01")

        # Assert
        self.vaga_validador_mock.valida_data_aplicacao.assert_called_once_with(
            "2025-06-01"
        )

    def test_validacao_data_aplicacao_erro(self):
        """Testa validação de data de aplicação com erro"""
        # Arrange
        self.vaga_validador_mock.valida_data_aplicacao.side_effect = (
            DataInvalidaException()
        )

        # Act & Assert
        with pytest.raises(DataInvalidaException):
            self.validador_service.VALIDADORES["data_aplicaçao"]("01/06/2025")

        self.vaga_validador_mock.valida_data_aplicacao.assert_called_once_with(
            "01/06/2025"
        )

    def test_validacao_nome_empresa(self):
        """Testa validação de nome de empresa"""
        # Act
        self.validador_service.VALIDADORES["nome_empresa"]("TechCorp")

        # Assert
        self.empresa_validador_mock.valida_nome_empresa.assert_called_once_with(
            "TechCorp"
        )

    def test_validacao_site_empresa(self):
        """Testa validação de site de empresa"""
        # Act
        self.validador_service.VALIDADORES["site_empresa"]("https://techcorp.com")

        # Assert
        self.empresa_validador_mock.valida_link_empresa.assert_called_once_with(
            "https://techcorp.com"
        )

    def test_validacao_setor_empresa(self):
        """Testa validação de setor de empresa (sempre válido)"""
        # Act
        resultado = self.validador_service.VALIDADORES["setor_empresa"]("Tecnologia")

        # Assert
        assert resultado is True
