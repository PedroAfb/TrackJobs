import curses
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from trackJobs.exceptions import RetornarMenuException
from trackJobs.visualizacao import MenuVisualizacao
from trackJobs.visualizacao import visualizacao_candidatura


@pytest.fixture
def mock_tela():
    tela = MagicMock()
    tela.getmaxyx.return_value = (20, 80)  # Mock terminal size
    return tela


@pytest.fixture
def mock_candidatura():
    return {
        "titulo": "Desenvolvedor Python",
        "empresa": "TechCorp",
        "localizacao": "Remoto",
        "descricao": "Desenvolvimento de aplicações web.",
        "id": 1,
        "idEmpresa": 2,
    }


def test_set_conteudo(mock_tela, mock_candidatura):
    menu = MenuVisualizacao(mock_tela)
    menu.set_conteudo(mock_candidatura)

    assert "Titulo:" in menu.conteudo
    assert "Desenvolvedor Python" in menu.conteudo
    assert "Empresa:" in menu.conteudo
    assert "TechCorp" in menu.conteudo
    assert "Localizacao:" in menu.conteudo
    assert "Remoto" in menu.conteudo
    assert "Descricao:" in menu.conteudo
    assert "Desenvolvimento de aplicações web." in menu.conteudo
    assert "id" not in menu.conteudo
    assert "idEmpresa" not in menu.conteudo


def test_exibir_campo(mock_tela):
    menu = MenuVisualizacao(mock_tela)
    conteudo = ["Titulo:", "Desenvolvedor Python", "", "Empresa:", "TechCorp"]
    scroll = 0

    menu.exibir_campo(conteudo, scroll)

    mock_tela.clear.assert_called_once()
    mock_tela.addstr.assert_any_call(0, 2, "Titulo:", curses.A_BOLD)
    mock_tela.addstr.assert_any_call(1, 2, "Desenvolvedor Python")
    mock_tela.addstr.assert_any_call(3, 2, "Empresa:", curses.A_BOLD)
    mock_tela.addstr.assert_any_call(4, 2, "TechCorp")
    mock_tela.addstr.assert_any_call(
        19, 2, "⬆⬇ para rolar, aperte ESC para voltar.", curses.A_DIM
    )


def test_menu_da_candidatura(mock_tela, mock_candidatura):
    menu = MenuVisualizacao(mock_tela)
    menu.set_conteudo(mock_candidatura)

    with patch.object(
        mock_tela, "getch", side_effect=[curses.KEY_DOWN, curses.KEY_UP, 27]
    ):
        menu.menu_da_candidatura(mock_candidatura)

    assert mock_tela.clear.call_count > 0
    assert mock_tela.addstr.call_count > 0


def test_visualizacao_candidatura_simple(mock_tela):
    with patch("trackJobs.visualizacao.get_vaga") as mock_get_vaga, patch(
        "trackJobs.visualizacao.MenuVisualizacao.escolha_candidatura"
    ) as mock_escolha_candidatura:
        mock_escolha_candidatura.return_value = {"link": "http://example.com/vaga1"}
        mock_get_vaga.return_value = {
            "titulo": "Desenvolvedor Python",
            "empresa": "TechCorp",
            "localizacao": "Remoto",
            "descricao": "Desenvolvimento de aplicações web.",
        }

        # Limit the loop by raising RetornarMenuException after one iteration
        with patch(
            "trackJobs.visualizacao.MenuVisualizacao.menu_da_candidatura",
            side_effect=RetornarMenuException,
        ):
            visualizacao_candidatura(mock_tela)

        mock_escolha_candidatura.assert_called_once()
        mock_get_vaga.assert_called_once_with(
            "track_jobs.db", "http://example.com/vaga1"
        )
