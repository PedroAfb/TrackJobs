from unittest.mock import patch

from .db_test import criar_banco_teste_com_dados
from .db_test import remove_banco_teste
from .test_menu import setup_tela_mock
from .test_menu import verifica_saida_esperada
from trackJobs.menu import FILTROS
from trackJobs.status import edita_status
from trackJobs.status import MenuStatus
from trackJobs.utils import get_candidaturas


@patch.object(MenuStatus, "menu_candidaturas", return_value=4)
@patch.object(MenuStatus, "menu_status", return_value="entrevista")
def test_edicao_status(mock_menu, mock_menu_status, esperado_mensagem_sucesso):
    criar_banco_teste_com_dados()
    with open("saida_teste.txt", "w") as saida:
        with patch("curses.curs_set"):
            tela_mock = setup_tela_mock(saida)
            edita_status(tela_mock, db_path="track_jobs_test.db")

    mock_menu.assert_called_once()
    mock_menu_status.assert_called_once()

    verifica_saida_esperada(esperado_mensagem_sucesso)

    candidatura_alterada = get_candidaturas(
        "track_jobs_test.db", filtro="DevOps Engineer", tipo_filtro=FILTROS["nome"]
    )
    assert candidatura_alterada[0]["status"] == "entrevista"

    remove_banco_teste()
