from unittest.mock import Mock

import pytest

from trackJobs.exceptions import CampoDuplicadoException
from trackJobs.exceptions import NomeVazioException
from trackJobs.exceptions import URLInvalidaException
from trackJobs.exceptions import URLJaCadastradaException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.services.validadores.empresa_validador_service import (
    EmpresaValidadorService,
)


class TestEmpresaValidadorService:
    """Testes unitários para o EmpresaValidadorService"""

    def setup_method(self):
        """Setup para cada teste - cria mock para o repository"""
        self.empresa_repository_mock = Mock()
        self.validador = EmpresaValidadorService(self.empresa_repository_mock)

    def test_valida_nome_empresa_valido(self):
        """Testa validação de nome de empresa válido"""
        # Arrange
        self.empresa_repository_mock.buscar_empresa_por_nome.return_value = None

        # Act
        resultado = self.validador.valida_nome_empresa("TechCorp")

        # Assert
        assert resultado is True
        self.empresa_repository_mock.buscar_empresa_por_nome.assert_called_once_with(
            "TechCorp"
        )

    def test_valida_nome_empresa_vazio(self):
        """Testa validação de nome de empresa vazio"""
        # Act & Assert
        with pytest.raises(NomeVazioException):
            self.validador.valida_nome_empresa("")

        self.empresa_repository_mock.buscar_empresa_por_nome.assert_not_called()

    def test_valida_nome_empresa_duplicado(self):
        """Testa validação de nome de empresa duplicado"""
        # Arrange
        self.empresa_repository_mock.buscar_empresa_por_nome.return_value = Empresa(
            id=1, nome="TechCorp"
        )

        # Act & Assert
        with pytest.raises(CampoDuplicadoException) as excinfo:
            self.validador.valida_nome_empresa("TechCorp")

        assert "Empresa já cadastrada" in str(excinfo.value)
        self.empresa_repository_mock.buscar_empresa_por_nome.assert_called_once_with(
            "TechCorp"
        )

    def test_valida_link_empresa_valido(self):
        """Testa validação de link de empresa válido"""
        # Arrange
        self.empresa_repository_mock.buscar_empresa_por_link.return_value = None

        # Act
        resultado = self.validador.valida_link_empresa("https://techcorp.com")

        # Assert
        assert resultado is True
        self.empresa_repository_mock.buscar_empresa_por_link.assert_called_once_with(
            "https://techcorp.com"
        )

    def test_valida_link_empresa_vazio(self):
        """Testa validação de link de empresa vazio (opcional)"""
        # Act
        resultado = self.validador.valida_link_empresa("")

        # Assert
        assert resultado is True
        self.empresa_repository_mock.buscar_empresa_por_link.assert_not_called()

    def test_valida_link_empresa_invalido(self):
        """Testa validação de link de empresa inválido"""
        # Act & Assert
        with pytest.raises(URLInvalidaException):
            self.validador.valida_link_empresa("techcorp")

        self.empresa_repository_mock.buscar_empresa_por_link.assert_not_called()

    def test_valida_link_empresa_duplicado(self):
        """Testa validação de link de empresa duplicado"""
        # Arrange
        self.empresa_repository_mock.buscar_empresa_por_link.return_value = Empresa(
            id=1, nome="TechCorp", site="https://techcorp.com"
        )

        # Act & Assert
        with pytest.raises(URLJaCadastradaException):
            self.validador.valida_link_empresa("https://techcorp.com")

        self.empresa_repository_mock.buscar_empresa_por_link.assert_called_once_with(
            "https://techcorp.com"
        )
