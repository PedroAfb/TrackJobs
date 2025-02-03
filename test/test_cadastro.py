from db_test import criar_banco_teste, remove_banco_teste
from unittest.mock import patch
from trackJobs.exceptions import RetornarMenuException
from trackJobs.cadastro import cadastra_candidatura, obter_link_vaga
import pytest
import sqlite3

# Testes sem o cadastro de empresa
def test_cadastro_vaga_sem_empresa(dict_cadastro_sucesso_sem_empresa, capsys):
    with patch("trackJobs.cadastro.coleta_dados_vaga", return_value=dict_cadastro_sucesso_sem_empresa):
        criar_banco_teste()

        cadastra_candidatura(db_path="track_jobs_test.db")
        captured_stdout = capsys.readouterr()
        assert "Cadastro realizado com sucesso!" in captured_stdout.out

    remove_banco_teste()

def test_cadastro_vaga_sem_empresa_link_duplicado(
    dict_cadastro_sucesso_sem_empresa,
    dict_cadastro_sem_empresa_link_duplicado,
    capsys):
    with patch("trackJobs.cadastro.coleta_dados_vaga", return_value=dict_cadastro_sucesso_sem_empresa):
        criar_banco_teste()

        cadastra_candidatura(db_path="track_jobs_test.db")
        captured_stdout = capsys.readouterr()
        assert "Cadastro realizado com sucesso!" in captured_stdout.out

    with patch("trackJobs.cadastro.coleta_dados_vaga", return_value=dict_cadastro_sem_empresa_link_duplicado):
        with pytest.raises(sqlite3.IntegrityError):
            cadastra_candidatura(db_path="track_jobs_test.db", teste=True)
        captured_stdout = capsys.readouterr()
        assert "Erro ao cadastrar no banco de dados: vagas.link já foi cadastrada!" in captured_stdout.out

    remove_banco_teste()

@pytest.mark.parametrize("mock_input, expected_output", [
    (["invalid_url", "https://vaga.com/456"], "https://vaga.com/456"),  # Primeira inválida, depois válida
    (["6"], RetornarMenuException),  # Usuário deseja sair
])
def test_obter_link_vaga(mock_input, expected_output):
    criar_banco_teste()
    with patch("trackJobs.cadastro.Prompt.ask", side_effect=mock_input):
        if expected_output == RetornarMenuException:
            with pytest.raises(RetornarMenuException):  # Verifica se a exceção foi levantada
                obter_link_vaga(db_path="track_jobs_test.db")
        else:
            assert obter_link_vaga(db_path="track_jobs_test.db") == expected_output  # Verifica se retornou o link correto
    remove_banco_teste()





'''
Cadastro com sucesso
link duplicado
link com formato inválido
'''
#Testes com o cadastro de empresa
'''
cadastro com sucesso
nome duplicado
link duplicado
link com formato inválido
'''