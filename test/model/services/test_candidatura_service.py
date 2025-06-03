from unittest.mock import Mock

import pytest

from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.services.candidatura_service import CandidaturaService


class TestCandidaturaService:
    """Testes unitários para o CandidaturaService"""

    def setup_method(self):
        """Setup para cada teste - cria mocks para os repositories"""
        self.empresa_repository_mock = Mock()
        self.vaga_repository_mock = Mock()
        self.candidatura_service = CandidaturaService(
            self.empresa_repository_mock, self.vaga_repository_mock
        )

    def test_cadastra_candidatura_sem_empresa(self):
        """Testa cadastro de vaga sem empresa associada"""
        # Arrange
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            empresa=None,
        )
        # Act
        self.candidatura_service.cadastra_candidatura(vaga)
        # Assert
        self.vaga_repository_mock.cadastrar_candidatura.assert_called_once_with(vaga)
        self.empresa_repository_mock.cadastrar_empresa.assert_not_called()
        self.empresa_repository_mock.buscar_empresa_por_nome.assert_not_called()

    def test_cadastra_candidatura_com_empresa_nova(self):
        """Testa cadastro de vaga com uma empresa nova"""
        # Arrange
        empresa = Empresa(
            nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
        )
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            empresa=empresa,
        )
        # Configure o mock para simular que a empresa não existe
        self.empresa_repository_mock.buscar_empresa_por_nome.return_value = None
        self.empresa_repository_mock.cadastrar_empresa.return_value = (
            1  # ID da nova empresa
        )
        # Act
        self.candidatura_service.cadastra_candidatura(vaga)
        # Assert
        self.empresa_repository_mock.buscar_empresa_por_nome.assert_called_once_with(
            empresa.nome
        )
        self.empresa_repository_mock.cadastrar_empresa.assert_called_once_with(empresa)
        self.vaga_repository_mock.cadastrar_candidatura.assert_called_once_with(vaga)
        assert vaga.empresa.id == 1  # Verifica se o ID da empresa foi atualizado

    def test_cadastra_candidatura_com_empresa_existente(self):
        """Testa cadastro de vaga com uma empresa já existente"""
        # Arrange
        empresa_existente = Empresa(
            id=2, nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
        )
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            empresa=Empresa(nome="TechCorp"),  # Apenas o nome é necessário para busca
        )
        # Configure o mock para simular que a empresa já existe
        self.empresa_repository_mock.buscar_empresa_por_nome.return_value = (
            empresa_existente
        )
        # Act
        self.candidatura_service.cadastra_candidatura(vaga)
        # Assert
        self.empresa_repository_mock.buscar_empresa_por_nome.assert_called_once_with(
            vaga.empresa.nome
        )
        # Não deve chamar cadastro de empresa
        self.empresa_repository_mock.cadastrar_empresa.assert_not_called()
        self.vaga_repository_mock.cadastrar_candidatura.assert_called_once_with(vaga)

    def test_cadastra_candidatura_erro_no_repository(self):
        """Testa erro no repository durante cadastro"""
        # Arrange
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            empresa=None,
        )
        # Configura o mock para lançar uma exceção
        self.vaga_repository_mock.cadastrar_candidatura.side_effect = (
            TrackJobsException("Erro ao cadastrar vaga")
        )
        # Act & Assert
        with pytest.raises(TrackJobsException) as excinfo:
            self.candidatura_service.cadastra_candidatura(vaga)
        assert "Erro ao cadastrar vaga" in str(excinfo.value)
