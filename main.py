import curses
import sqlite3

import questionary
from rich.console import Console
from rich.panel import Panel

from trackJobs.cadastro import cadastra_candidatura
from trackJobs.edicao import edicao
from trackJobs.exceptions import InicializacaoBancoException
from trackJobs.remocao import remocao
from trackJobs.status import edita_status
from trackJobs.utils import CUSTOM_STYLE
from trackJobs.visualizacao import visualizacao_candidatura

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4

console = Console()


def inicializa_banco():
    try:
        conexao = sqlite3.connect("track_jobs.db")
        cursor = conexao.cursor()

        cursor.execute(
            """create table if not exists empresas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            site TEXT,
            setor TEXT
            )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'candidatar-se'
            CHECK(status IN
            ('candidatar-se', 'em análise', 'entrevista', 'rejeitado', 'aceito')),
            data de aplicaçao DATE DEFAULT CURRENT_DATE,
            descriçao TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY(idEmpresa) REFERENCES empresas(id)
            )"""
        )

        conexao.close()

    except Exception as e:
        console.print(f"[bold yellow]Erro técnico:[/bold yellow] {str(e)}")
        raise InicializacaoBancoException("Erro ao inicializar o banco de dados")


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


menu()
