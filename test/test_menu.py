import os
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from .db_test import criar_banco_teste_com_dados
from .db_test import remove_banco_teste
from trackJobs.menu import CANDIDATURA_SELECIONADA
from trackJobs.menu import FILTROS
from trackJobs.menu import Menu
from trackJobs.utils import get_candidaturas


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
            Menu(tela_mock).menu_candidaturas(candidaturas)

    esperado_printado = request.getfixturevalue(esperado)
    verifica_saida_esperada(esperado_printado)

    remove_banco_teste()


@pytest.mark.parametrize(
    "filtro, tipo_filtro, esperado",
    [
        ("Desenvolvedor", FILTROS["nome"], "esperado_candidaturas_filtradas_por_nome"),
        (
            "jobs.example.com/1",
            FILTROS["link"],
            "esperado_candidaturas_filtradas_por_link",
        ),
        (
            "candidatar-se",
            FILTROS["status"],
            "esperado_candidaturas_filtradas_por_status",
        ),
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
            Menu(tela_mock).menu_candidaturas(candidaturas)

    verifica_saida_esperada(esperado_candidaturas)
    remove_banco_teste()
