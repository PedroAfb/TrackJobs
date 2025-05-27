import curses
import sqlite3

from rich.console import Console

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.controller.job_controller import JobController
from trackJobs.model.job_model import JobModel
from trackJobs.view.cli import CliView

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4

console = Console()


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


def menu(tela):
    inicializa_banco()
    job_model = JobModel()
    job_controller = JobController(job_model)
    cli_view = CliView(job_controller, tela)
    cli_view.menu_principal()

    db = BancoDeDados()
    db.close_conexao()


if __name__ == "__main__":
    curses.wrapper(menu)
