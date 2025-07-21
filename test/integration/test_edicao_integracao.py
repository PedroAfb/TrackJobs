from unittest.mock import Mock
from unittest.mock import patch

import pytest

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.view.edicao_cli import EdicaoCliView


class TestEdicaoIntegracao:
    """Testes de integração para a funcionalidade de edição"""

    def setup_method(self):
        """Setup para cada teste"""
        self.tela_mock = Mock()
        self.tela_mock.getmaxyx.return_value = (24, 80)

        # Mock do controller com comportamento mais realista
        self.controller_mock = Mock(spec=JobController)

        # Dados de teste
        self.empresa_teste = Empresa(
            id=1, nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
        )

        self.vaga_teste = {
            "id": 1,
            "nome": "Desenvolvedor Python",
            "link": "https://example.com/vaga",
            "status": "aplicado",
            "data_aplicacao": "2025-07-21",
            "descricao": "Vaga para desenvolvedor Python sênior",
            "nome_empresa": "TechCorp",
            "site_empresa": "https://techcorp.com",
            "setor_empresa": "Tecnologia",
        }

    @patch("trackJobs.view.edicao_cli.questionary.text")
    @patch("curses.curs_set")
    def test_edicao_completa_sucesso(self, mock_curs_set, mock_questionary):
        """Testa o fluxo completo de edição com sucesso"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        # Simula escolha da candidatura
        with patch.object(
            edicao_view.menu_edicao, "escolha_candidatura"
        ) as mock_escolha:
            mock_escolha.return_value = self.vaga_teste

            # Simula escolha do campo
            with patch.object(edicao_view.menu_edicao, "menu_edicao") as mock_menu:
                mock_menu.return_value = "status"

                # Simula entrada do usuário
                mock_questionary.return_value.ask.return_value = "entrevistado"

                # Simula validação bem-sucedida
                self.controller_mock.validar_campo.return_value = True

                # Mock da mensagem de sucesso
                with patch.object(
                    edicao_view.menu_edicao, "exibe_mensagem_sucesso"
                ) as mock_sucesso:
                    # Act
                    edicao_view.edicao()

                    # Assert
                    mock_escolha.assert_called_once()
                    mock_menu.assert_called_once_with(self.vaga_teste)
                    self.controller_mock.validar_campo.assert_called_once_with(
                        "status", "entrevistado"
                    )
                    self.controller_mock.atualizar_candidatura.assert_called_once_with(
                        self.vaga_teste, "status", "entrevistado"
                    )
                    mock_sucesso.assert_called_once_with(None, "Status")

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_edicao_com_validacao_multipla(self, mock_questionary):
        """Testa edição com múltiplas tentativas de validação"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        # Simula múltiplas entradas do usuário
        mock_questionary.return_value.ask.side_effect = [
            "data_invalida",  # primeira tentativa inválida
            "2025-13-45",  # segunda tentativa inválida
            "2025-12-31",  # terceira tentativa válida
        ]

        # Simula validações
        self.controller_mock.validar_campo.side_effect = [
            "Data deve estar no formato YYYY-MM-DD",
            "Data inválida",
            True,
        ]

        with patch.object(
            edicao_view.menu_edicao, "escolha_candidatura"
        ) as mock_escolha:
            mock_escolha.return_value = self.vaga_teste

            with patch.object(edicao_view.menu_edicao, "menu_edicao") as mock_menu:
                mock_menu.return_value = "data_aplicacao"

                with patch.object(edicao_view.menu_edicao, "exibe_mensagem_sucesso"):
                    # Act
                    edicao_view.edicao()

                    # Assert
                    assert mock_questionary.call_count == 3
                    assert self.controller_mock.validar_campo.call_count == 3
                    self.controller_mock.atualizar_candidatura.assert_called_once_with(
                        self.vaga_teste, "data_aplicacao", "2025-12-31"
                    )

    def test_edicao_cancelamento_usuario(self):
        """Testa cancelamento da edição pelo usuário"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        with patch.object(
            edicao_view.menu_edicao, "escolha_candidatura"
        ) as mock_escolha:
            # Simula usuário pressionando ESC
            mock_escolha.side_effect = RetornarMenuException()

            # Act
            edicao_view.edicao()  # Não deve lançar exceção

            # Assert
            self.controller_mock.atualizar_candidatura.assert_not_called()

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_edicao_erro_atualizacao(self, mock_questionary):
        """Testa erro durante atualização da candidatura"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        mock_questionary.return_value.ask.return_value = "https://link-duplicado.com"
        self.controller_mock.validar_campo.return_value = True

        # Simula erro no controller
        erro_esperado = TrackJobsException("Link já está em uso por outra vaga")
        self.controller_mock.atualizar_candidatura.side_effect = erro_esperado

        with patch.object(
            edicao_view.menu_edicao, "escolha_candidatura"
        ) as mock_escolha:
            mock_escolha.return_value = self.vaga_teste

            with patch.object(edicao_view.menu_edicao, "menu_edicao") as mock_menu:
                mock_menu.return_value = "link"

                with patch.object(
                    edicao_view.menu_edicao, "exibe_mensagem_erro"
                ) as mock_erro:
                    # Act
                    edicao_view.edicao()

                    # Assert
                    mock_erro.assert_called_once_with(str(erro_esperado))

    @patch("trackJobs.view.edicao_cli.questionary.text")
    @pytest.mark.parametrize(
        "campo,novo_valor,campo_capitalizado",
        [
            ("nome", "Senior Python Developer", "Nome"),
            ("link", "https://nova-vaga.com/123", "Link"),
            ("data_aplicacao", "2025-08-15", "Data_aplicacao"),
            ("status", "rejeitado", "Status"),
            ("descricao", "Nova descrição da vaga", "Descricao"),
        ],
    )
    def test_edicao_diferentes_campos(
        self, mock_questionary, campo, novo_valor, campo_capitalizado
    ):
        """Testa edição de diferentes campos"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        mock_questionary.return_value.ask.return_value = novo_valor
        self.controller_mock.validar_campo.return_value = True

        with patch.object(
            edicao_view.menu_edicao, "escolha_candidatura"
        ) as mock_escolha:
            mock_escolha.return_value = self.vaga_teste

            with patch.object(edicao_view.menu_edicao, "menu_edicao") as mock_menu:
                mock_menu.return_value = campo

                with patch.object(
                    edicao_view.menu_edicao, "exibe_mensagem_sucesso"
                ) as mock_sucesso:
                    # Act
                    edicao_view.edicao()

                    # Assert
                    self.controller_mock.atualizar_candidatura.assert_called_with(
                        self.vaga_teste, campo, novo_valor
                    )
                    mock_sucesso.assert_called_with(None, campo_capitalizado)

    @patch("trackJobs.view.edicao_cli.questionary.text")
    def test_edicao_valores_com_espacos(self, mock_questionary):
        """Testa que valores com espaços são tratados corretamente"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        # Simula entrada com espaços no início e fim
        mock_questionary.return_value.ask.return_value = "  Novo valor com espaços  "
        self.controller_mock.validar_campo.return_value = True

        with patch.object(
            edicao_view.menu_edicao, "escolha_candidatura"
        ) as mock_escolha:
            mock_escolha.return_value = self.vaga_teste

            with patch.object(edicao_view.menu_edicao, "menu_edicao") as mock_menu:
                mock_menu.return_value = "nome"

                with patch.object(edicao_view.menu_edicao, "exibe_mensagem_sucesso"):
                    # Act
                    edicao_view.edicao()

                    # Assert
                    # Verifica se os espaços foram removidos
                    self.controller_mock.validar_campo.assert_called_with(
                        "nome", "Novo valor com espaços"
                    )
                    self.controller_mock.atualizar_candidatura.assert_called_with(
                        self.vaga_teste, "nome", "Novo valor com espaços"
                    )

    def test_edicao_compatibilidade_curses(self):
        """Testa compatibilidade com interface curses"""
        # Arrange
        edicao_view = EdicaoCliView(self.tela_mock, self.controller_mock)

        # Verifica se a view tem acesso ao objeto tela (necessário para curses)
        assert edicao_view.tela == self.tela_mock
        assert hasattr(edicao_view, "menu_edicao")

        # Verifica se o menu_edicao também tem acesso à tela
        assert hasattr(edicao_view.menu_edicao, "tela")
