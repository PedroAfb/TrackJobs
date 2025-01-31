from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.panel import Panel
import sqlite3
from exceptions import InicializacaoBancoException, CadastroBancoException
from cadastro import cadastra_candidatura

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2 
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4
DATA_NULA = '0/0/0'

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
            data_aplicacao DATE,
            status TEXT DEFAULT 'em análise',
            descricao TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY(idEmpresa) REFERENCES empresas(id)
            )"""
            )

        conexao.close()

    except Exception as e:
        console.print(
            "[bold red]Erro ao inicializar o banco de dados.[/bold red] Verifique se há problemas de permissão ou formato do banco."
        )
        console.print(f"[bold yellow]Erro técnico:[/bold yellow] {str(e)}")
        console.print("[bold red]Encerrando o programa...[/bold red]")
        raise InicializacaoBancoException("Erro ao inicializar o banco de dados")


def main():
    inicializa_banco()

    while True:
        console.print(Panel("[bold magenta]TrackJobs - Gerenciador de Candidaturas[/bold magenta]", expand=False))

        msg_prompt = (
            "[bold cyan]Escolha uma opção abaixo:[/bold cyan]\n\n"
            "[green]1[/green] - Cadastrar Candidatura\n"
            "[green]2[/green] - Editar Status da Candidatura\n"
            "[green]3[/green] - Editar Candidatura\n"
            "[green]4[/green] - Remover Candidatura\n"
            "[green]5[/green] - Fechar Ferramenta\n"
        )
        opcao = IntPrompt.ask(msg_prompt, choices=['1', '2', '3', '4', '5'])

        if opcao == CADASTRAR_CANDIDATURA:
            cadastra_candidatura()
        elif opcao == EDITAR_STATUS:
            pass
        elif opcao == EDITAR_CANDIDATURA:
            pass
        elif opcao == REMOVER_CANDIDATURA:
            pass
        else:
            break

main()