from unittest.mock import Mock
from unittest.mock import patch

import pytest

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.exceptions import TrackJobsException
from trackJobs.view.edicao_cli import EdicaoCliView


class TestEdicaoCliView:
    """Testes unitários para EdicaoCliView"""

    def setup_method(self):
        """Setup para cada teste"""
        self.tela_mock = Mock()
        self.controller_mock = Mock(spec=JobController)
        self.menu_edicao_mock = Mock()

        # Mock do MenuEdicao constructor
        self.menu_edicao_patch = patch(
            "trackJobs.view.edicao_cli.MenuEdicao", return_value=self.menu_edicao_mock
        )
        self.menu_edicao_constructor = self.menu_edicao_patch.start()

        self.edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

    def teardown_method(self):
        """Cleanup após cada teste"""
        self.menu_edicao_patch.stop()

    def test_init(self):
        """Testa inicialização da EdicaoCliView"""
        assert self.edicao_view.tela == self.tela_mock
        assert self.edicao_view.controller == self.controller_mock
        assert self.edicao_view.menu_edicao == self.menu_edicao_mock
        assert hasattr(self.edicao_view, "console")

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_solicitar_novo_valor_com_validacao_sucesso(self, mock_questionary):
        """Testa solicitação de novo valor com validação bem-sucedida"""
        # Arrange
        mock_questionary.return_value.ask.return_value = "Novo valor  "
        self.controller_mock.validar_campo.return_value = True

        # Act
        resultado = self.edicao_view._solicitar_novo_valor("nome")

        # Assert
        assert resultado == "Novo valor"
        mock_questionary.assert_called_once()
        self.controller_mock.validar_campo.assert_called_once_with("nome", "Novo valor")

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_solicitar_novo_valor_com_validacao_erro_depois_sucesso(
        self, mock_questionary
    ):
        """Testa solicitação de novo valor com erro de validação depois sucesso"""
        # Arrange
        mock_questionary.return_value.ask.side_effect = [
            "valor_invalido",
            "valor_valido",
        ]
        self.controller_mock.validar_campo.side_effect = ["Erro de validação", True]

        # Act
        resultado = self.edicao_view._solicitar_novo_valor("status")

        # Assert
        assert resultado == "valor_valido"
        assert mock_questionary.call_count == 2
        assert self.controller_mock.validar_campo.call_count == 2

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_edicao_sucesso_completo(self, mock_questionary):
        """Testa edição completa com sucesso"""
        # Arrange
        candidatura_mock = {"nome": "Dev Python", "status": "aplicado"}
        self.menu_edicao_mock.escolha_candidatura.return_value = candidatura_mock
        self.menu_edicao_mock.menu_edicao.return_value = "status"

        mock_questionary.return_value.ask.return_value = "entrevistado"
        self.controller_mock.validar_campo.return_value = True

        # Act
        self.edicao_view.edicao()

        # Assert
        self.menu_edicao_mock.escolha_candidatura.assert_called_once()
        self.menu_edicao_mock.menu_edicao.assert_called_once_with(candidatura_mock)
        self.controller_mock.validar_campo.assert_called_once_with(
            "status", "entrevistado"
        )
        self.controller_mock.atualizar_candidatura.assert_called_once_with(
            candidatura_mock, "status", "entrevistado"
        )
        self.menu_edicao_mock.exibe_mensagem_sucesso.assert_called_once_with(
            None, "Status"
        )

    def test_edicao_com_retornar_menu_exception(self):
        """Testa edição quando usuário volta ao menu"""
        # Arrange
        self.menu_edicao_mock.escolha_candidatura.side_effect = RetornarMenuException()

        # Act & Assert - não deve lançar exceção
        self.edicao_view.edicao()

        # Assert
        self.controller_mock.atualizar_candidatura.assert_not_called()
        self.menu_edicao_mock.exibe_mensagem_sucesso.assert_not_called()

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_edicao_com_track_jobs_exception(self, mock_questionary):
        """Testa edição com erro de negócio"""
        # Arrange
        candidatura_mock = {"nome": "Dev Python", "status": "aplicado"}
        self.menu_edicao_mock.escolha_candidatura.return_value = candidatura_mock
        self.menu_edicao_mock.menu_edicao.return_value = "link"

        mock_questionary.return_value.ask.return_value = "link_duplicado"
        self.controller_mock.validar_campo.return_value = True

        erro_esperado = TrackJobsException("Link já existe")
        self.controller_mock.atualizar_candidatura.side_effect = erro_esperado

        # Act
        self.edicao_view.edicao()

        # Assert
        self.menu_edicao_mock.exibe_mensagem_erro.assert_called_once_with(
            str(erro_esperado)
        )
        self.menu_edicao_mock.exibe_mensagem_sucesso.assert_not_called()

    @patch("trackJobs.view.edicao_cli.questionary.text")
    @pytest.mark.parametrize(
        "campo,valor",
        [
            ("nome", "Novo nome da vaga"),
            ("link", "https://novo-link.com"),
            ("data_aplicacao", "2025-12-31"),
            ("descricao", "Nova descrição"),
        ],
    )
    def test_edicao_campos_diferentes(self, mock_questionary, campo, valor):
        """Testa edição de diferentes campos"""
        # Arrange
        candidatura_mock = {campo: "valor_antigo"}
        self.menu_edicao_mock.escolha_candidatura.return_value = candidatura_mock
        self.menu_edicao_mock.menu_edicao.return_value = campo

        mock_questionary.return_value.ask.return_value = valor
        self.controller_mock.validar_campo.return_value = True

        # Act
        self.edicao_view.edicao()

        # Assert
        self.controller_mock.atualizar_candidatura.assert_called_with(
            candidatura_mock, campo, valor
        )

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_solicitar_novo_valor_multiplos_erros(self, mock_questionary):
        """Testa solicitação com múltiplos erros de validação"""
        # Arrange
        mock_questionary.return_value.ask.side_effect = [
            "erro1",
            "erro2",
            "erro3",
            "valor_correto",
        ]
        self.controller_mock.validar_campo.side_effect = [
            "Primeiro erro",
            "Segundo erro",
            "Terceiro erro",
            True,
        ]

        # Act
        resultado = self.edicao_view._solicitar_novo_valor("nome")

        # Assert
        assert resultado == "valor_correto"
        assert mock_questionary.call_count == 4
        assert self.controller_mock.validar_campo.call_count == 4

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_solicitar_novo_valor_campo_com_espacos(self, mock_questionary):
        """Testa solicitação que remove espaços em branco"""
        # Arrange
        mock_questionary.return_value.ask.return_value = "  valor com espacos  "
        self.controller_mock.validar_campo.return_value = True

        # Act
        resultado = self.edicao_view._solicitar_novo_valor("descricao")

        # Assert
        assert resultado == "valor com espacos"
        self.controller_mock.validar_campo.assert_called_once_with(
            "descricao", "valor com espacos"
        )
