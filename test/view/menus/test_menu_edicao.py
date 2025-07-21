import curses
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.view.menus.menu_edicao import CAMPOS_DISPLAY
from trackJobs.view.menus.menu_edicao import CAMPOS_VAGA
from trackJobs.view.menus.menu_edicao import MenuEdicao


class TestMenuEdicao:
    """Testes unitários para MenuEdicao"""

    def setup_method(self):
        """Setup para cada teste"""
        self.tela_mock = Mock()
        self.tela_mock.getmaxyx.return_value = (24, 80)  # altura, largura
        self.controller_mock = Mock(spec=JobController)

        # Cria o menu_edicao e define a tela manualmente
        self.menu_edicao = MenuEdicao(self.tela_mock, self.controller_mock)
        self.menu_edicao.tela = self.tela_mock
        self.menu_edicao.controller = self.controller_mock

    def test_init(self):
        """Testa inicialização do MenuEdicao"""
        assert self.menu_edicao.index_campo_atual == 0

    def test_exibir_campo_normal(self):
        """Testa exibição de campo normal (não selecionado)"""
        # Arrange
        campo = "nome"
        dados = "Desenvolvedor Python"
        i = 0
        campo_pra_print = 1  # Diferente do index_campo_atual (0)

        # Act
        self.menu_edicao.exibir_campo(campo, dados, i, campo_pra_print)

        # Assert
        self.tela_mock.addstr.assert_called_once()
        call_args = self.tela_mock.addstr.call_args[0]
        assert call_args[0] == 2  # i + 2
        assert call_args[1] == 2  # coluna
        assert "Nome" in call_args[2]  # mensagem contém o nome capitalizado
        assert call_args[3] == curses.A_NORMAL  # estilo normal

    def test_exibir_campo_selecionado(self):
        """Testa exibição de campo selecionado"""
        # Arrange
        campo = "status"
        dados = "aplicado"
        i = 0
        campo_pra_print = 0  # Igual ao index_campo_atual (0)

        # Act
        self.menu_edicao.exibir_campo(campo, dados, i, campo_pra_print)

        # Assert
        self.tela_mock.addstr.assert_called_once()
        call_args = self.tela_mock.addstr.call_args[0]
        assert "Status: aplicado" in call_args[2]  # mostra valor quando selecionado
        assert call_args[3] == curses.A_REVERSE  # estilo reverso

    def test_exibir_campo_com_display_personalizado(self):
        """Testa exibição de campo com nome de exibição personalizado"""
        # Arrange
        campo = "data_aplicacao"
        dados = "2025-07-21"
        i = 0
        campo_pra_print = 1

        # Act
        self.menu_edicao.exibir_campo(campo, dados, i, campo_pra_print)

        # Assert
        call_args = self.tela_mock.addstr.call_args[0]
        assert "Data de aplicação" in call_args[2]  # usa CAMPOS_DISPLAY

    def test_exibir_campo_descricao_personalizada(self):
        """Testa exibição de campo descrição com acento"""
        # Arrange
        campo = "descricao"
        dados = "Descrição da vaga"
        i = 0
        campo_pra_print = 1

        # Act
        self.menu_edicao.exibir_campo(campo, dados, i, campo_pra_print)

        # Assert
        call_args = self.tela_mock.addstr.call_args[0]
        assert "Descrição" in call_args[2]  # usa CAMPOS_DISPLAY

    def test_interpreta_teclado_mover_baixo(self):
        """Testa movimento para baixo no menu"""
        # Arrange
        self.tela_mock.getch.return_value = 258  # KEY_DOWN
        self.menu_edicao.index_campo_atual = 0

        # Act
        resultado = self.menu_edicao.interpreta_teclado_menu_edicao()

        # Assert
        assert self.menu_edicao.index_campo_atual == 1
        assert resultado is None

    def test_interpreta_teclado_mover_cima(self):
        """Testa movimento para cima no menu"""
        # Arrange
        self.tela_mock.getch.return_value = 259  # KEY_UP
        self.menu_edicao.index_campo_atual = 2

        # Act
        resultado = self.menu_edicao.interpreta_teclado_menu_edicao()

        # Assert
        assert self.menu_edicao.index_campo_atual == 1
        assert resultado is None

    def test_interpreta_teclado_mover_baixo_limite(self):
        """Testa que não move além do último campo"""
        # Arrange
        self.tela_mock.getch.return_value = 258  # KEY_DOWN
        self.menu_edicao.index_campo_atual = len(CAMPOS_VAGA) - 1
        index_original = self.menu_edicao.index_campo_atual

        # Act
        resultado = self.menu_edicao.interpreta_teclado_menu_edicao()

        # Assert
        assert self.menu_edicao.index_campo_atual == index_original  # não mudou
        assert resultado is None

    def test_interpreta_teclado_mover_cima_limite(self):
        """Testa que não move acima do primeiro campo"""
        # Arrange
        self.tela_mock.getch.return_value = 259  # KEY_UP
        self.menu_edicao.index_campo_atual = 0

        # Act
        resultado = self.menu_edicao.interpreta_teclado_menu_edicao()

        # Assert
        assert self.menu_edicao.index_campo_atual == 0  # não mudou
        assert resultado is None

    def test_interpreta_teclado_selecionar(self):
        """Testa seleção de campo"""
        # Arrange
        self.tela_mock.getch.return_value = 10  # ENTER
        self.menu_edicao.index_campo_atual = 2

        # Act
        resultado = self.menu_edicao.interpreta_teclado_menu_edicao()

        # Assert
        assert resultado == CAMPOS_VAGA[2]
        self.tela_mock.clear.assert_called_once()

    def test_interpreta_teclado_voltar(self):
        """Testa volta ao menu principal"""
        # Arrange
        self.tela_mock.getch.return_value = 27  # ESC

        # Act & Assert
        with pytest.raises(RetornarMenuException):
            self.menu_edicao.interpreta_teclado_menu_edicao()

        self.tela_mock.clear.assert_called_once()

    def test_exibir_menu_edicao(self):
        """Testa exibição do menu de edição"""
        # Arrange
        candidatura = {
            "nome": "Dev Python",
            "link": "https://example.com",
            "data_aplicacao": "2025-07-21",
            "status": "aplicado",
            "descricao": "Vaga para desenvolvedor",
        }
        itens_exibidos = 10
        posicao_scroll = 0

        with patch.object(self.menu_edicao, "ajustar_scroll", return_value=0):
            with patch.object(self.menu_edicao, "exibir_campo") as mock_exibir:
                # Act
                self.menu_edicao.exibir_menu_edicao(
                    candidatura, itens_exibidos, posicao_scroll
                )

                # Assert
                self.tela_mock.addstr.assert_called_once()  # mensagem de cabeçalho
                assert mock_exibir.call_count == len(CAMPOS_VAGA)

    @patch("curses.curs_set")
    def test_menu_edicao_loop(self, mock_curs_set):
        """Testa o loop principal do menu de edição"""
        # Arrange
        candidatura = {
            "nome": "Test",
            "link": "test.com",
            "data_aplicacao": None,
            "status": "aplicado",
            "descricao": None,
        }

        # Simula seleção do primeiro campo
        self.tela_mock.getch.return_value = 10  # ENTER

        with patch.object(self.menu_edicao, "exibir_menu_edicao"):
            # Act
            resultado = self.menu_edicao.menu_edicao(candidatura)

            # Assert
            assert resultado == CAMPOS_VAGA[0]  # retorna o primeiro campo
            mock_curs_set.assert_called_with(0)
            self.tela_mock.keypad.assert_called_with(True)

    def test_exibe_mensagem_sucesso_campo_normal(self):
        """Testa exibição de mensagem de sucesso para campo normal"""
        # Arrange
        campo = "nome"

        # Act
        self.menu_edicao.exibe_mensagem_sucesso(None, campo)

        # Assert
        assert self.tela_mock.addstr.call_count == 2  # duas mensagens
        primeira_chamada = self.tela_mock.addstr.call_args_list[0][0]
        assert "Nome atualizado com sucesso" in primeira_chamada[2]

    def test_exibe_mensagem_sucesso_campo_com_display(self):
        """Testa exibição de mensagem de sucesso para campo com display personalizado"""
        # Arrange
        campo = "data_aplicacao"

        # Act
        self.menu_edicao.exibe_mensagem_sucesso(None, campo)

        # Assert
        primeira_chamada = self.tela_mock.addstr.call_args_list[0][0]
        assert "Data de aplicação atualizado com sucesso" in primeira_chamada[2]

    def test_campos_vaga_constante(self):
        """Testa que os campos da vaga estão definidos corretamente"""
        assert "nome" in CAMPOS_VAGA
        assert "link" in CAMPOS_VAGA
        assert "data_aplicacao" in CAMPOS_VAGA
        assert "status" in CAMPOS_VAGA
        assert "descricao" in CAMPOS_VAGA

    def test_campos_display_constante(self):
        """Testa que o mapeamento de exibição está correto"""
        assert CAMPOS_DISPLAY["data_aplicacao"] == "data de aplicação"
        assert CAMPOS_DISPLAY["descricao"] == "descrição"
