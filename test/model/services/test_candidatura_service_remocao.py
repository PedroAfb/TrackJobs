from unittest.mock import Mock

import pytest

from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.services.candidatura_service import CandidaturaService


class TestCandidaturaServiceRemocao:
    def setup_method(self):
        """Setup para cada teste"""
        self.empresa_repository_mock = Mock()
        self.vaga_repository_mock = Mock()
        self.service = CandidaturaService(
            self.empresa_repository_mock, self.vaga_repository_mock
        )

    def test_remove_vaga_sucesso(self):
        """Testa remoção de vaga com sucesso"""
        # Arrange
        vaga = Vaga(
            id=1, nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )

        # Act
        self.service.remove_vaga(vaga)

        # Assert
        self.vaga_repository_mock.remover_vaga.assert_called_once_with(vaga)

    def test_remove_vaga_com_empresa_associada(self):
        """Testa remoção de vaga que tem empresa associada"""
        # Arrange
        from trackJobs.model.entities.empresa import Empresa

        empresa = Empresa(id=1, nome="TechCorp", site="https://techcorp.com")
        vaga = Vaga(
            id=1,
            nome="Dev Python",
            link="https://example.com/vaga",
            status="aplicado",
            empresa=empresa,
        )

        # Act
        self.service.remove_vaga(vaga)

        # Assert
        self.vaga_repository_mock.remover_vaga.assert_called_once_with(vaga)

    def test_remove_vaga_erro_no_repository(self):
        """Testa erro no repository durante remoção"""
        # Arrange
        vaga = Vaga(
            id=1, nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.remover_vaga.side_effect = TrackJobsException(
            "Erro ao remover vaga do banco de dados"
        )

        # Act & Assert
        with pytest.raises(TrackJobsException) as exc_info:
            self.service.remove_vaga(vaga)

        assert "Erro ao remover vaga do banco de dados" in str(exc_info.value)
        self.vaga_repository_mock.remover_vaga.assert_called_once_with(vaga)

    def test_remove_vaga_none(self):
        """Testa tentativa de remoção com vaga None"""
        # Act
        self.service.remove_vaga(None)

        # Assert - Deve passar a vaga None para o repository
        # O repository deve ser responsável por tratar esse caso
        self.vaga_repository_mock.remover_vaga.assert_called_once_with(None)

    @pytest.mark.parametrize(
        "vaga_id,nome,link,status",
        [
            (1, "Desenvolvedor Backend", "https://example.com/backend", "aplicado"),
            (2, "Analista de Dados", "https://example.com/data", "entrevista"),
            (3, "DevOps Engineer", "https://example.com/devops", "rejeitado"),
        ],
    )
    def test_remove_vaga_diferentes_vagas(self, vaga_id, nome, link, status):
        """Testa remoção de diferentes tipos de vagas"""
        # Arrange
        vaga = Vaga(id=vaga_id, nome=nome, link=link, status=status)

        # Act
        self.service.remove_vaga(vaga)

        # Assert
        self.vaga_repository_mock.remover_vaga.assert_called_once_with(vaga)

    def test_remove_vaga_repositorio_indisponivel(self):
        """Testa remoção quando repository lança erro de conexão"""
        # Arrange
        vaga = Vaga(
            id=1, nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.remover_vaga.side_effect = Exception(
            "Conexão perdida"
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.service.remove_vaga(vaga)

        assert "Conexão perdida" in str(exc_info.value)
