import os
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from .db_test import criar_banco_teste_com_dados
from .db_test import remove_banco_teste
from trackJobs.status import CANDIDATURA_SELECIONADA
from trackJobs.status import edita_status
from trackJobs.status import FILTRO_LINK
from trackJobs.status import FILTRO_NOME
from trackJobs.status import FILTRO_STATUS
from trackJobs.status import get_candidaturas
from trackJobs.status import menu_candidaturas


def setup_tela_mock(saida):
    def fake_addstr(y, x, text, *args):
        saida.write(text + "\n")

    tela_mock = MagicMock()
    tela_mock.getch.return_value = CANDIDATURA_SELECIONADA
    tela_mock.addstr = fake_addstr
    with patch("curses.curs_set"):
        tela_mock.getmaxyx.return_value = (20, 80)
    return tela_mock


def verifica_saida_esperada(esperado, arquivo="saida_teste.txt"):
    with open(arquivo, "r") as f:
        printed_lines = f.readlines()
        printed_lines = [line.strip() for line in printed_lines]
    assert esperado == printed_lines
    if os.path.exists(arquivo):
        os.remove(arquivo)


@patch("trackJobs.status.menu_candidaturas", return_value=3)
@patch("trackJobs.status.menu_status", return_value="entrevista")
def test_edicao_status(mock_atualiza_cand, mock_menu_status, esperado_status_printado):
    criar_banco_teste_com_dados()

    with open("saida_teste.txt", "w") as saida:
        with patch("curses.curs_set"):
            tela_mock = setup_tela_mock(saida)
            edita_status(tela_mock, db_path="track_jobs_test.db")

    mock_atualiza_cand.assert_called_once()
    mock_menu_status.assert_called_once()

    verifica_saida_esperada(esperado_status_printado)

    candidatura = get_candidaturas(
        "track_jobs_test.db", filtro="Desenvolvedor Mobile", tipo_filtro=FILTRO_NOME
    )
    assert candidatura[0]["status"] == "entrevista"

    remove_banco_teste()


@pytest.mark.parametrize(
    "candidaturas, esperado",
    [
        ([], "esperado_nenhuma_candidatura_printada"),
        ("todas_candidaturas", "esperado_todas_candidaturas_printadas"),
    ],
)
def test_candidaturas(candidaturas, esperado, request):
    criar_banco_teste_com_dados()
    candidaturas = (
        request.getfixturevalue(candidaturas)
        if isinstance(candidaturas, str)
        else candidaturas
    )

    with open("saida_teste.txt", "w") as saida:
        with patch("curses.curs_set"):
            tela_mock = setup_tela_mock(saida)
            menu_candidaturas(tela_mock, candidaturas)

    esperado_printado = request.getfixturevalue(esperado)
    verifica_saida_esperada(esperado_printado)

    remove_banco_teste()


@pytest.mark.parametrize(
    "filtro, tipo_filtro, esperado",
    [
        ("Desenvolvedor", FILTRO_NOME, "esperado_candidaturas_filtradas_por_nome"),
        ("jobs.example.com/1", FILTRO_LINK, "esperado_candidaturas_filtradas_por_link"),
        ("candidatar-se", FILTRO_STATUS, "esperado_candidaturas_filtradas_por_status"),
    ],
)
def test_status_mostra_candidaturas_com_filtros(filtro, tipo_filtro, esperado, request):
    criar_banco_teste_com_dados()
    candidaturas = get_candidaturas(
        "track_jobs_test.db", filtro=filtro, tipo_filtro=tipo_filtro
    )
    esperado_candidaturas = request.getfixturevalue(esperado)

    with open("saida_teste.txt", "w") as saida:
        with patch("curses.curs_set"):
            tela_mock = setup_tela_mock(saida)
            menu_candidaturas(tela_mock, candidaturas)

    verifica_saida_esperada(esperado_candidaturas)
    remove_banco_teste()
