from unittest.mock import Mock
from unittest.mock import patch

import pytest

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.vaga import Vaga


class TestJobController:
    """Testes unitários para o JobController"""

    def setup_method(self):
        """Setup para cada teste - cria mock para o JobModel"""
        self.job_model_mock = Mock()
        self.controller = JobController(self.job_model_mock)

    def test_campos_perguntas_vaga(self):
        """Testa se os campos da vaga são retornados corretamente"""
        # Arrange
        self.job_model_mock.campos_cadastro_vaga.return_value = [
            "nome",
            "link",
            "status",
        ]
        # Act
        resultado = self.controller.campos_perguntas_vaga()
        # Assert
        assert "nome" in resultado
        assert "link" in resultado
        assert "status" in resultado
        assert resultado["nome"] == "Qual o nome da vaga?[OBRIGATÓRIO]\n"
        assert resultado["link"] == "Qual o link da vaga?[OBRIGATÓRIO]\n"
        assert resultado["status"] == "Qual o status da vaga?\n"
        self.job_model_mock.campos_cadastro_vaga.assert_called_once()

    def test_campos_perguntas_empresa(self):
        """Testa se os campos da empresa são retornados corretamente"""
        # Arrange
        self.job_model_mock.campos_cadastro_empresa.return_value = [
            "nome_empresa",
            "site_empresa",
            "setor_empresa",
        ]
        # Act
        resultado = self.controller.campos_perguntas_empresa()
        # Assert
        assert "nome_empresa" in resultado
        assert "site_empresa" in resultado
        assert "setor_empresa" in resultado
        self.job_model_mock.campos_cadastro_empresa.assert_called_once()

    def test_validar_campo_valido(self):
        """Testa validação de campo com valor válido"""
        # Arrange
        self.job_model_mock.validar_campo.return_value = True
        # Act
        resultado = self.controller.validar_campo("nome", "Desenvolvedor Python")
        # Assert
        assert resultado is True
        self.job_model_mock.validar_campo.assert_called_once_with(
            "nome", "Desenvolvedor Python"
        )

    def test_validar_campo_invalido(self):
        """Testa validação de campo com valor inválido"""
        # Arrange
        self.job_model_mock.validar_campo.side_effect = TrackJobsException(
            "Nome não pode estar vazio"
        )
        # Act
        resultado = self.controller.validar_campo("nome", "")
        # Assert
        assert resultado == "[bold red]Nome não pode estar vazio[/bold red]"
        self.job_model_mock.validar_campo.assert_called_once_with("nome", "")

    def test_obter_opcoes_empresa(self):
        """Testa obtenção das opções de empresa"""
        # Arrange
        self.job_model_mock.listar_nome_empresas.return_value = [
            "TechCorp",
            "HealthTech",
        ]
        # Act
        opcoes = self.controller.obter_opcoes_empresa()
        # Assert
        assert len(opcoes) == 4  # 2 empresas + 2 opções fixas
        assert "Não atrelar empresa" in opcoes
        assert "Cadastrar nova empresa" in opcoes
        assert "TechCorp" in opcoes
        assert "HealthTech" in opcoes
        self.job_model_mock.listar_nome_empresas.assert_called_once()

    @pytest.mark.parametrize(
        "escolha, tipo_esperado, dados_esperados",
        [
            ("Não atrelar empresa", "nenhuma", None),
            ("Cadastrar nova empresa", "nova", None),
            ("TechCorp", "existente", "TechCorp"),
        ],
    )
    def test_processar_escolha_empresa(self, escolha, tipo_esperado, dados_esperados):
        """Testa processamento da escolha de empresa"""
        # Act
        resultado = self.controller.processar_escolha_empresa(escolha)
        # Assert
        assert resultado["tipo"] == tipo_esperado
        assert resultado["dados"] == dados_esperados

    def test_cadastra_candidatura_sucesso(self):
        """Testa cadastro de candidatura com sucesso"""
        # Arrange
        dados_vaga = {
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "candidatar-se",
        }
        # Mock para dictionary_to_vaga
        vaga_mock = Mock(spec=Vaga)
        with patch(
            "trackJobs.controller.job_controller.dictionary_to_vaga",
            return_value=vaga_mock,
        ):
            # Act
            resultado = self.controller.cadastra_candidatura(dados_vaga)
            # Assert
            assert "[bold green]" in resultado
            assert "Cadastro da vaga realizado com sucesso" in resultado
            self.job_model_mock.cadastro.assert_called_once_with(vaga_mock)

    def test_cadastra_candidatura_erro(self):
        """Testa cadastro de candidatura com erro"""
        # Arrange
        dados_vaga = {
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "candidatar-se",
        }
        vaga_mock = Mock(spec=Vaga)
        erro = TrackJobsException("Erro ao cadastrar vaga: link já existe")
        with patch(
            "trackJobs.controller.job_controller.dictionary_to_vaga",
            return_value=vaga_mock,
        ):
            self.job_model_mock.cadastro.side_effect = erro
            # Act & Assert
            with pytest.raises(TrackJobsException) as excinfo:
                self.controller.cadastra_candidatura(dados_vaga)
            assert "Erro ao cadastrar vaga" in str(excinfo.value)
            self.job_model_mock.cadastro.assert_called_once_with(vaga_mock)
