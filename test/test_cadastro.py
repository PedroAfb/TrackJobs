import sqlite3
from unittest.mock import patch

import pytest

from .db_test import criar_banco_teste
from .db_test import remove_banco_teste
from trackJobs.cadastro import cadastra_candidatura
from trackJobs.cadastro import obter_link_vaga
from trackJobs.cadastro import obter_site_empresa
from trackJobs.exceptions import RetornarMenuException


# Testes sem o cadastro de empresa
def realiza_cadastro_sem_empresa_com_sucesso(dados_candidatura):
    with patch("trackJobs.cadastro.coleta_dados_vaga", return_value=dados_candidatura):
        cadastra_candidatura(db_path="track_jobs_test.db")


def test_cadastro_vaga_sem_empresa(dict_cadastro_sem_empresa, capsys):
    criar_banco_teste()
    realiza_cadastro_sem_empresa_com_sucesso(dict_cadastro_sem_empresa)
    captured_stdout = capsys.readouterr()
    assert "Cadastro da vaga realizado com sucesso!" in captured_stdout.out

    remove_banco_teste()


def test_cadastro_vaga_sem_empresa_link_duplicado(
    dict_cadastro_sem_empresa, dict_cadastro_sem_empresa_link_duplicado, capsys
):
    criar_banco_teste()
    # Realiza o primeiro cadastro
    realiza_cadastro_sem_empresa_com_sucesso(dict_cadastro_sem_empresa)
    captured_stdout = capsys.readouterr()
    assert "Cadastro da vaga realizado com sucesso!" in captured_stdout.out

    # Realiza o segundo cadastro tentando cadastrar o mesmo link
    with patch(
        "trackJobs.cadastro.coleta_dados_vaga",
        return_value=dict_cadastro_sem_empresa_link_duplicado,
    ):
        with pytest.raises(sqlite3.IntegrityError):
            cadastra_candidatura(db_path="track_jobs_test.db", teste=True)
        captured_stdout = capsys.readouterr()
        assert (
            "Erro ao cadastrar no banco de dados: vagas.link já foi cadastrada!"
            in captured_stdout.out
        )

    remove_banco_teste()


@pytest.mark.parametrize(
    "mock_input, expected_output",
    [
        (
            ["invalid_url", "https://vaga.com/456"],
            "https://vaga.com/456",
        ),  # Primeira inválida, depois válida
        (["6"], RetornarMenuException),  # Usuário deseja sair
    ],
)
def test_validacao_link_vaga_no_prompt(mock_input, expected_output):
    """
    Testa a validação do link da vaga durante a entrada do usuário no prompt.

    - Se o link for inválido ou duplicado, a função deve levantar RetornarMenuException.
    - Se o link for válido, a função deve retornar corretamente o link informado.

    """
    criar_banco_teste()
    with patch("trackJobs.cadastro.Prompt.ask", side_effect=mock_input):
        if expected_output == RetornarMenuException:
            with pytest.raises(
                RetornarMenuException
            ):  # Verifica se a exceção foi levantada
                obter_link_vaga(db_path="track_jobs_test.db")
        else:
            assert (
                obter_link_vaga(db_path="track_jobs_test.db") == expected_output
            )  # Verifica se retornou o link correto
    remove_banco_teste()


# Testes com o cadastro de empresa
def realiza_cadastro_com_empresa(dados_candidatura):
    with patch(
        "trackJobs.cadastro.coleta_dados_vaga", return_value=dados_candidatura
    ), patch(
        "trackJobs.cadastro.coleta_dados_empresa",
        return_value=("https://example.com", "Tech"),
    ) as mock_dados_empresa:
        cadastra_candidatura(db_path="track_jobs_test.db")

    return mock_dados_empresa


def test_cadastro_vaga_com_empresa_n_cadastrada(dict_cadastro_com_empresa, capsys):
    criar_banco_teste()
    realiza_cadastro_com_empresa(dict_cadastro_com_empresa)
    captured_stdout = capsys.readouterr()
    assert "Cadastro da empresa realizado com sucesso" in captured_stdout.out
    assert "Cadastro da vaga realizado com sucesso!" in captured_stdout.out

    remove_banco_teste()


def test_cadastro_vaga_com_empresa_cadastrada(
    dict_cadastro_com_empresa, dict_cadastro_com_empresa2, capsys
):
    criar_banco_teste()
    # Realiza o primeiro cadastro
    realiza_cadastro_com_empresa(dict_cadastro_com_empresa)
    captured_stdout = capsys.readouterr()
    assert "Cadastro da empresa realizado com sucesso" in captured_stdout.out
    assert "Cadastro da vaga realizado com sucesso!" in captured_stdout.out

    # Realiza outro cadastro de vaga com a mesma empresa
    funcao_coleta_dados_empresa = realiza_cadastro_com_empresa(
        dict_cadastro_com_empresa2
    )

    captured_stdout = capsys.readouterr()
    assert "Cadastro da vaga realizado com sucesso!" in captured_stdout.out
    funcao_coleta_dados_empresa.assert_not_called()

    remove_banco_teste()


def test_site_invalido_empresa(capsys):
    criar_banco_teste()
    prompt_input = ["invalid_url", "https://vaga.com/456"]
    expected_output = "URL inválida. Digite um link válido ou deixe em branco."

    with patch("trackJobs.cadastro.Prompt.ask", side_effect=prompt_input):
        conexao = sqlite3.connect("track_jobs_test.db")
        cursor = conexao.cursor()

        obter_site_empresa(cursor)
        captured_stdout = capsys.readouterr()
        assert expected_output in captured_stdout.out

    remove_banco_teste()


def test_site_duplicado_empresa(dict_cadastro_com_empresa, capsys):
    criar_banco_teste()
    prompt_input = ["https://example.com", "https://example23.com"]
    expected_output = (
        "Essa URL já foi cadastrada. Digite um link válido ou deixe em branco."
    )

    realiza_cadastro_com_empresa(dict_cadastro_com_empresa)
    with patch("trackJobs.cadastro.Prompt.ask", side_effect=prompt_input):
        conexao = sqlite3.connect("track_jobs_test.db")
        cursor = conexao.cursor()

        obter_site_empresa(cursor)
        captured_stdout = capsys.readouterr()
        assert expected_output in captured_stdout.out

    remove_banco_teste()
