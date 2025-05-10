from unittest.mock import patch

import pytest
from rich.console import Console

from .db_test import criar_banco_teste_com_dados
from .db_test import remove_banco_teste
from trackJobs.validador import VALIDADORES


@pytest.mark.parametrize(
    "campo_selecionado, novo_dado, esperado_valido",
    [
        ("nome", "", False),  # Nome vazio
        ("nome", "Desenvolvedor Backend", True),  # Nome válido
        ("link", "invalid-url", False),  # URL inválida
        ("link", "https://jobs.example.com/valid", True),  # URL válida
        ("status", "inexistente", False),  # Status inválido
        ("status", "aceito", True),  # Status válido
        ("data_aplicaçao", "2021-02-30", False),  # Data inválida
        ("data_aplicaçao", "2023-10-10", True),  # Data válida
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
