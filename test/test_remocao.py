from unittest.mock import MagicMock
from unittest.mock import patch

from .db_test import criar_banco_teste_com_dados
from .db_test import remove_banco_teste
from .test_menu import setup_tela_mock
from .test_menu import verifica_saida_esperada
from trackJobs.exceptions import RetornarMenuException
from trackJobs.menu import FILTROS
from trackJobs.remocao import MenuRemocao
from trackJobs.remocao import remocao
from trackJobs.utils import get_candidaturas


@patch.object(MenuRemocao, "menu_candidaturas", return_value=2)
def test_remocao_success(MockMenuRemocao, esperado_msg_remocao_sucesso):
    criar_banco_teste_com_dados()
    link_vaga_escolhida = "'https://jobs.example.com/4'"
    candidatura_escolhida = get_candidaturas(
        "track_jobs_test.db", link_vaga_escolhida, FILTROS["link"]
    )

    assert candidatura_escolhida is not None

    with patch("questionary.confirm") as mock_confirm:
        mock_confirm.return_value.ask.return_value = True
        with open("saida_teste.txt", "w") as saida:
            with patch("curses.curs_set"):
                tela_mock = setup_tela_mock(saida)
                remocao(tela_mock, "track_jobs_test.db")

    candidatura_escolhida = get_candidaturas(
        "track_jobs_test.db", link_vaga_escolhida, FILTROS["link"]
    )

    assert not candidatura_escolhida
    verifica_saida_esperada(esperado_msg_remocao_sucesso)
    remove_banco_teste()


@patch("trackJobs.remocao.MenuRemocao")
@patch("trackJobs.remocao.filtra_candidaturas")
def test_remocao_retornar_menu_exception(MockMenuRemocao, mock_filtra_candidaturas):
    mock_menu_remocao = MockMenuRemocao.return_value
    mock_menu_remocao.menu_candidaturas.side_effect = RetornarMenuException
    mock_tela = MagicMock()
    db_path = "track_jobs_test.db"
    remocao(mock_tela, db_path)

    mock_menu_remocao.exibe_mensagem_erro.assert_not_called()
