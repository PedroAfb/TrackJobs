import curses
import sqlite3

import questionary
from rich.console import Console
from rich.panel import Panel

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.cadastro import cadastra_candidatura
from trackJobs.edicao import edicao
from trackJobs.remocao import remocao
from trackJobs.status import edita_status
from trackJobs.utils import CUSTOM_STYLE
from trackJobs.visualizacao import visualizacao_candidatura

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4

console = Console()


# TODO: Criar uma classe para o banco de dados
def inicializa_banco():
    try:
        banco = BancoDeDados()
        banco.inicializa_banco()
    except sqlite3.Error as e:
        console.print(
            "[bold red]Erro ao conectar ao banco de dados:[/bold red]",
            str(e),
        )
        exit(1)


def menu():
    inicializa_banco()

    while True:
        console.print(
            Panel(
                "[bold magenta]TrackJobs - Gerenciador de Candidaturas[/bold magenta]",
                expand=False,
            )
        )

        opcao = questionary.select(
            "Escolha uma opção abaixo:\n",
            choices=[
                "Cadastrar Candidatura",
                "Visualizar Candidaturas",
                "Editar Status da Candidatura",
                "Editar Candidatura",
                "Remover Candidatura",
                "Fechar Ferramenta",
            ],
            style=CUSTOM_STYLE,
        ).ask()

        if opcao == "Cadastrar Candidatura":
            cadastra_candidatura()
        elif opcao == "Visualizar Candidaturas":
            curses.wrapper(visualizacao_candidatura)
        elif opcao == "Editar Status da Candidatura":
            curses.wrapper(edita_status)
        elif opcao == "Editar Candidatura":
            curses.wrapper(edicao)
        elif opcao == "Remover Candidatura":
            curses.wrapper(remocao)
        else:
            break

    db = BancoDeDados()
    db.close_conexao()


menu()
