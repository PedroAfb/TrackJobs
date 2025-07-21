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
        assert resultado == "Nome não pode estar vazio"
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

    # ========== TESTES PARA FUNCIONALIDADES DE EDIÇÃO ==========

    def test_validar_campo_sucesso(self):
        """Testa validação de campo com sucesso"""
        # Arrange
        self.job_model_mock.validar_campo.return_value = True

        # Act
        resultado = self.controller.validar_campo("nome", "Desenvolvedor Python")

        # Assert
        assert resultado is True
        self.job_model_mock.validar_campo.assert_called_once_with(
            "nome", "Desenvolvedor Python"
        )

    def test_validar_campo_erro_validacao(self):
        """Testa validação de campo com erro"""
        # Arrange
        erro_esperado = TrackJobsException("Nome deve ter pelo menos 3 caracteres")
        self.job_model_mock.validar_campo.side_effect = erro_esperado

        # Act
        resultado = self.controller.validar_campo("nome", "AB")

        # Assert
        assert resultado == "Nome deve ter pelo menos 3 caracteres"
        self.job_model_mock.validar_campo.assert_called_once_with("nome", "AB")

    @patch("trackJobs.controller.job_controller.vaga_to_dictionary")
    def test_obter_dados_vaga_sucesso(self, mock_vaga_to_dict):
        """Testa obtenção de dados da vaga com sucesso"""
        # Arrange
        vaga_mock = Mock(spec=Vaga)
        expected_dict = {
            "id": 1,
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "aplicado",
            "data_aplicacao": "2025-07-21",
            "descricao": "Vaga para desenvolvedor",
        }

        self.job_model_mock.get_vaga_por_link.return_value = vaga_mock
        mock_vaga_to_dict.return_value = expected_dict

        # Act
        resultado = self.controller.obter_dados_vaga("https://example.com/vaga")

        # Assert
        assert resultado == expected_dict
        self.job_model_mock.get_vaga_por_link.assert_called_once_with(
            "https://example.com/vaga"
        )
        mock_vaga_to_dict.assert_called_once_with(vaga_mock)

    @patch("trackJobs.controller.job_controller.dictionary_to_vaga")
    def test_atualizar_candidatura_sucesso(self, mock_dictionary_to_vaga):
        """Testa atualização de candidatura com sucesso"""
        # Arrange
        dados_vaga = {
            "id": 1,
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "aplicado",
        }

        vaga_mock = Mock(spec=Vaga)
        mock_dictionary_to_vaga.return_value = vaga_mock

        # Act
        resultado = self.controller.atualizar_candidatura(
            dados_vaga, "status", "entrevistado"
        )

        # Assert
        expected_message = (
            "[bold green]\nAtualização da vaga realizada com sucesso!\n[/bold green]"
        )
        assert resultado == expected_message

        mock_dictionary_to_vaga.assert_called_once_with(dados_vaga)
        self.job_model_mock.atualizar_vaga.assert_called_once_with(
            vaga_mock, "status", "entrevistado"
        )

    @patch("trackJobs.controller.job_controller.dictionary_to_vaga")
    def test_atualizar_candidatura_erro_model(self, mock_dictionary_to_vaga):
        """Testa atualização de candidatura com erro no model"""
        # Arrange
        dados_vaga = {
            "id": 1,
            "nome": "Test",
            "link": "https://test.com",
            "status": "aplicado",
        }
        vaga_mock = Mock(spec=Vaga)

        mock_dictionary_to_vaga.return_value = vaga_mock

        erro_esperado = TrackJobsException(
            "Campo 'data_aplicacao' não é válido para atualização."
        )
        self.job_model_mock.atualizar_vaga.side_effect = erro_esperado

        # Act & Assert
        with pytest.raises(TrackJobsException) as excinfo:
            self.controller.atualizar_candidatura(
                dados_vaga, "data_aplicacao", "2025-13-45"
            )

        assert (
            str(excinfo.value)
            == "Campo 'data_aplicacao' não é válido para atualização."
        )
        self.job_model_mock.atualizar_vaga.assert_called_once_with(
            vaga_mock, "data_aplicacao", "2025-13-45"
        )

    @patch("trackJobs.controller.job_controller.vaga_to_dictionary")
    def test_candidaturas_filtradas_sucesso(self, mock_vaga_to_dictionary):
        """Testa listagem de candidaturas filtradas"""
        # Arrange
        vaga1 = Mock(spec=Vaga)
        vaga2 = Mock(spec=Vaga)

        dict1 = {
            "id": 1,
            "nome": "Dev Python",
            "link": "https://test1.com",
            "status": "aplicado",
        }
        dict2 = {
            "id": 2,
            "nome": "Dev Java",
            "link": "https://test2.com",
            "status": "entrevista",
        }

        self.job_model_mock.candidaturas_filtradas.return_value = [vaga1, vaga2]
        mock_vaga_to_dictionary.side_effect = [dict1, dict2]

        # Act
        resultado = self.controller.candidaturas_filtradas("Python", "nome")

        # Assert
        assert resultado == [dict1, dict2]
        self.job_model_mock.candidaturas_filtradas.assert_called_once_with(
            "Python", "nome"
        )
        assert mock_vaga_to_dictionary.call_count == 2

    @pytest.mark.parametrize(
        "campo,valor,erro_esperado",
        [
            ("nome", "", "Nome não pode estar vazio"),
            ("link", "invalid-url", "URL inválida"),
            ("status", "invalido", "Status deve ser um dos valores válidos"),
            ("data_aplicacao", "2025-13-45", "Data inválida"),
        ],
    )
    def test_validar_campo_diferentes_erros(self, campo, valor, erro_esperado):
        """Testa validação de diferentes campos com diferentes erros"""
        # Arrange
        self.job_model_mock.validar_campo.side_effect = TrackJobsException(
            erro_esperado
        )

        # Act
        resultado = self.controller.validar_campo(campo, valor)

        # Assert
        assert resultado == erro_esperado
        self.job_model_mock.validar_campo.assert_called_once_with(campo, valor)

    @pytest.mark.parametrize(
        "campo,valor",
        [
            ("nome", "Desenvolvedor Python Sênior"),
            ("link", "https://empresa.com/vaga-123"),
            ("status", "entrevista"),
            ("data_aplicacao", "2025-12-31"),
            ("descricao", "Descrição detalhada da vaga"),
        ],
    )
    def test_validar_campo_diferentes_campos_validos(self, campo, valor):
        """Testa validação de diferentes campos com valores válidos"""
        # Arrange
        self.job_model_mock.validar_campo.return_value = True

        # Act
        resultado = self.controller.validar_campo(campo, valor)

        # Assert
        assert resultado is True
        self.job_model_mock.validar_campo.assert_called_once_with(campo, valor)
