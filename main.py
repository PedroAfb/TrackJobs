import curses
import sqlite3

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt

from trackJobs.cadastro import cadastra_candidatura
from trackJobs.edicao import edicao
from trackJobs.exceptions import InicializacaoBancoException
from trackJobs.status import edita_status

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
            data_aplicacao DATE DEFAULT CURRENT_DATE,
            descricao TEXT,
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

        msg_prompt = (
            "[bold cyan]Escolha uma opção abaixo:[/bold cyan]\n\n"
            "[green]1[/green] - Cadastrar Candidatura\n"
            "[green]2[/green] - Editar Status da Candidatura\n"
            "[green]3[/green] - Editar Candidatura\n"
            "[green]4[/green] - Remover Candidatura\n"
            "[green]5[/green] - Fechar Ferramenta\n"
        )
        opcao = IntPrompt.ask(msg_prompt, choices=["1", "2", "3", "4", "5"])

        if opcao == CADASTRAR_CANDIDATURA:
            cadastra_candidatura()
        elif opcao == EDITAR_STATUS:
            curses.wrapper(edita_status)
        elif opcao == EDITAR_CANDIDATURA:
            curses.wrapper(edicao)
        elif opcao == REMOVER_CANDIDATURA:
            pass
        else:
            break


menu()
