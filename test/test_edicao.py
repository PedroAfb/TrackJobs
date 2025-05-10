from unittest.mock import patch

import pytest
from rich.console import Console

from .db_test import criar_banco_teste_com_dados
from .db_test import remove_banco_teste
from .test_menu import setup_tela_mock
from .test_menu import verifica_saida_esperada
from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.edicao import edicao
from trackJobs.edicao import MenuEdicao
from trackJobs.menu import Menu
from trackJobs.validador import VALIDADORES


def get_vaga_id(db_path, id):
    db = BancoDeDados(db_path)
    cursor = db.cursor
    cursor.execute(f"SELECT * FROM vagas WHERE id = {id}")
    vaga = cursor.fetchone()
    if vaga:
        # Pega o nome das colunas
        colunas = [descricao[0] for descricao in cursor.description]

        # Cria um dicionário combinando as colunas com os valores
        vaga_dict = dict(zip(colunas, vaga))

        return vaga_dict
    else:
        return None  # Caso não encontre a vaga


@pytest.mark.parametrize(
    "campo_alterado, novo_valor, msg_esperada",
    [
        ("nome", "Dev Fullstack JR", "esperado_msg_edicao"),
        (
            "link",
            "https://jobs.example.com/25",
            "esperado_msg_link",
        ),
        (
            "data de aplicaçao",
            "2021-10-10",
            "esperado_msg_data",
        ),
        (
            "status",
            "rejeitado",
            "esperado_msg_status",
        ),
        (
            "descriçao",
            "Desenvolver novas features",
            "esperado_msg_descricao",
        ),
    ],
)
@patch.object(Menu, "menu_candidaturas", return_value=2)
def test_edicao(mock_menu, campo_alterado, novo_valor, msg_esperada, request):
    criar_banco_teste_com_dados()
    id_da_vaga_escolhida = "3"
    msg_esperada = request.getfixturevalue(msg_esperada)

    with patch.object(MenuEdicao, "menu_edicao", return_value=f"{campo_alterado}"):
        with patch("questionary.text") as mock_text:
            mock_text.return_value.ask.return_value = novo_valor
            with open("saida_teste.txt", "w") as saida:
                with patch("curses.curs_set"):
                    tela_mock = setup_tela_mock(saida)
                    edicao(tela_mock, db_path="track_jobs_test.db")

    verifica_saida_esperada(msg_esperada)

    candidatura_alterada = get_vaga_id("track_jobs_test.db", id_da_vaga_escolhida)
    assert candidatura_alterada[f"{campo_alterado}"] == novo_valor

    remove_banco_teste()


@pytest.mark.parametrize(
    "campo_selecionado, novo_dado, esperado_valido",
    [
        ("nome", "", False),  # Nome vazio
        ("nome", "Desenvolvedor Backend", True),  # Nome válido
        ("link", "invalid-url", False),  # URL inválida
        ("link", "https://jobs.example.com/valid", True),  # URL válida
        ("status", "inexistente", False),  # Status inválido
        ("status", "aceito", True),  # Status válido
        ("data de aplicaçao", "2021-02-30", False),  # Data inválida
        ("data de aplicaçao", "2023-10-10", True),  # Data válida
        ("descriçao", "", True),  # Descrição sempre válida
    ],
)
def test_validacao_dados_edicao(campo_selecionado, novo_dado, esperado_valido):
    criar_banco_teste_com_dados()
    with patch("questionary.text") as mock_text:
        mock_text.return_value.ask.return_value = novo_dado
        console = Console()
        valido = VALIDADORES[campo_selecionado](
            "track_jobs_test.db", novo_dado, console
        )
        assert valido == esperado_valido
    remove_banco_teste()
