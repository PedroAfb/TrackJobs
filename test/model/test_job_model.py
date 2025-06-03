from unittest.mock import patch

import pytest

from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.job_model import JobModel


class TestJobModel:
    """Testes unitários para o JobModel"""

    @patch("trackJobs.model.job_model.BancoDeDados")
    @patch("trackJobs.model.job_model.SQLiteEmpresaRepository")
    @patch("trackJobs.model.job_model.SQLiteVagaRepository")
    @patch("trackJobs.model.job_model.CandidaturaService")
    def test_cadastro_sucesso(
        self,
        candidatura_service_mock,
        vaga_repo_mock,
        empresa_repo_mock,
        banco_dados_mock,
    ):
        """Testa cadastro de candidatura com sucesso"""
        # Arrange
        banco_mock = banco_dados_mock.return_value
        empresa_repo = empresa_repo_mock.return_value
        vaga_repo = vaga_repo_mock.return_value
        service_mock = candidatura_service_mock.return_value

        model = JobModel(db_path="test.db")

        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
        )

        # Act
        model.cadastro(vaga)

        # Assert
        banco_dados_mock.assert_called_once_with("test.db")
        empresa_repo_mock.assert_called_once_with(banco_mock)
        vaga_repo_mock.assert_called_once_with(banco_mock)
        candidatura_service_mock.assert_called_once_with(empresa_repo, vaga_repo)
        service_mock.cadastra_candidatura.assert_called_once_with(vaga)

    @patch("trackJobs.model.job_model.BancoDeDados")
    @patch("trackJobs.model.job_model.SQLiteEmpresaRepository")
    @patch("trackJobs.model.job_model.SQLiteVagaRepository")
    @patch("trackJobs.model.job_model.CandidaturaService")
    def test_cadastro_erro(
        self,
        candidatura_service_mock,
        vaga_repo_mock,
        empresa_repo_mock,
        banco_dados_mock,
    ):
        """Testa cadastro de candidatura com erro"""
        # Arrange
        _ = banco_dados_mock.return_value
        _ = empresa_repo_mock.return_value
        _ = vaga_repo_mock.return_value
        service_mock = candidatura_service_mock.return_value

        model = JobModel(db_path="test.db")

        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
        )

        # Configurar o mock para lançar exceção
        error = TrackJobsException("Erro ao cadastrar vaga")
        service_mock.cadastra_candidatura.side_effect = error

        # Act & Assert
        with pytest.raises(TrackJobsException) as excinfo:
            model.cadastro(vaga)

        assert "Erro ao cadastrar vaga" in str(excinfo.value)
        service_mock.cadastra_candidatura.assert_called_once_with(vaga)

    @patch("trackJobs.model.job_model.BancoDeDados")
    @patch("trackJobs.model.job_model.SQLiteVagaRepository")
    def test_campos_cadastro_vaga(self, vaga_repo_mock, banco_dados_mock):
        """Testa obtenção dos campos para cadastro de vaga"""
        # Arrange
        banco_mock = banco_dados_mock.return_value
        vaga_repo = vaga_repo_mock.return_value
        vaga_repo.listar_campos_vaga.return_value = ["nome", "link", "status"]

        model = JobModel(db_path="test.db")

        # Act
        campos = model.campos_cadastro_vaga()

        # Assert
        assert campos == ["nome", "link", "status"]
        vaga_repo_mock.assert_called_once_with(banco_mock)
        vaga_repo.listar_campos_vaga.assert_called_once()

    @patch("trackJobs.model.job_model.BancoDeDados")
    @patch("trackJobs.model.job_model.SQLiteEmpresaRepository")
    def test_campos_cadastro_empresa(self, empresa_repo_mock, banco_dados_mock):
        """Testa obtenção dos campos para cadastro de empresa"""
        # Arrange
        banco_mock = banco_dados_mock.return_value
        empresa_repo = empresa_repo_mock.return_value
        empresa_repo.listar_campos_empresa.return_value = [
            "nome_empresa",
            "site_empresa",
            "setor_empresa",
        ]

        model = JobModel(db_path="test.db")

        # Act
        campos = model.campos_cadastro_empresa()

        # Assert
        assert campos == ["nome_empresa", "site_empresa", "setor_empresa"]
        empresa_repo_mock.assert_called_once_with(banco_mock)
        empresa_repo.listar_campos_empresa.assert_called_once()

    @patch("trackJobs.model.job_model.BancoDeDados")
    @patch("trackJobs.model.job_model.SQLiteEmpresaRepository")
    def test_listar_nome_empresas(self, empresa_repo_mock, banco_dados_mock):
        """Testa listagem de nomes de empresas"""
        # Arrange
        banco_mock = banco_dados_mock.return_value
        empresa_repo = empresa_repo_mock.return_value
        empresa_repo.listar_nome_empresas.return_value = ["TechCorp", "HealthTech"]

        model = JobModel(db_path="test.db")

        # Act
        empresas = model.listar_nome_empresas()

        # Assert
        assert empresas == ["TechCorp", "HealthTech"]
        empresa_repo_mock.assert_called_once_with(banco_mock)
        empresa_repo.listar_nome_empresas.assert_called_once()

    @patch("trackJobs.model.job_model.BancoDeDados")
    @patch("trackJobs.model.job_model.SQLiteEmpresaRepository")
    @patch("trackJobs.model.job_model.SQLiteVagaRepository")
    @patch("trackJobs.model.job_model.EmpresaValidadorService")
    @patch("trackJobs.model.job_model.VagaValidadorService")
    @patch("trackJobs.model.job_model.ValidadorService")
    def test_validar_campo(
        self,
        validador_service_mock,
        vaga_validador_mock,
        empresa_validador_mock,
        vaga_repo_mock,
        empresa_repo_mock,
        banco_dados_mock,
    ):
        """Testa validação de campo"""
        # Arrange
        banco_mock = banco_dados_mock.return_value
        empresa_repo = empresa_repo_mock.return_value
        vaga_repo = vaga_repo_mock.return_value
        empresa_validador = empresa_validador_mock.return_value
        vaga_validador = vaga_validador_mock.return_value
        validador_service = validador_service_mock.return_value

        validador_service.VALIDADORES = {"nome": lambda x: len(x) > 0}

        model = JobModel(db_path="test.db")

        # Act
        resultado = model.validar_campo("nome", "Desenvolvedor Python")

        # Assert
        assert resultado is True
        empresa_repo_mock.assert_called_once_with(banco_mock)
        vaga_repo_mock.assert_called_once_with(banco_mock)
        empresa_validador_mock.assert_called_once_with(empresa_repo)
        vaga_validador_mock.assert_called_once_with(vaga_repo)
        validador_service_mock.assert_called_once_with(
            empresa_validador, vaga_validador
        )
