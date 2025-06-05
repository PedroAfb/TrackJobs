# from unittest.mock import patch

# import pytest
# from rich.console import Console

# from trackJobs.model.repositories.SQLite.sqlite_empresa_repository import SQLiteEmpresaRepository
# from trackJobs.model.repositories.SQLite.sqlite_vaga_repository import SQLiteVagaRepository

# from .db_test import criar_banco_teste_com_dados
# from .db_test import remove_banco_teste
# from trackJobs.model.services.validadores.validador_service import ValidadorService
# from trackJobs.model.services.validadores.vaga_validador_service import VagaValidadorService
# from trackJobs.model.services.validadores.empresa_validador_service import EmpresaValidadorService
# from trackJobs.banco_de_dados import BancoDeDados


# @pytest.mark.parametrize(
#     "campo_selecionado, novo_dado, esperado_valido",
#     [
#         ("nome", "", False),  # Nome vazio
#         ("nome", "Desenvolvedor Backend", True),  # Nome válido
#         ("link", "invalid-url", False),  # URL inválida
#         ("link", "https://jobs.example.com/valid", True),  # URL válida
#         ("status", "inexistente", False),  # Status inválido
#         ("status", "aceito", True),  # Status válido
#         ("data_aplicaçao", "2021-02-30", False),  # Data inválida
#         ("data_aplicaçao", "2023-10-10", True),  # Data válida
#         ("descriçao", "", True),  # Descrição sempre válida
#     ],
# )
# def test_validacao_dados_edicao(campo_selecionado, novo_dado, esperado_valido):
#     criar_banco_teste_com_dados()
#     with patch("questionary.text") as mock_text:
#         mock_text.return_value.ask.return_value = novo_dado
#         console = Console()
#         empresa_validador = EmpresaValidadorService(SQLiteEmpresaRepository(BancoDeDados("track_jobs_test.db")))
#         vaga_validador = VagaValidadorService(SQLiteVagaRepository(BancoDeDados("track_jobs_test.db")))
#         validador_service = ValidadorService(empresa_validador, vaga_validador)
#         valido = validador_service.VALIDADORES[campo_selecionado](novo_dado)
#         assert valido == esperado_valido
#     remove_banco_teste()
