from rich.console import Console
from rich.prompt import IntPrompt
from rich.panel import Panel
import sqlite3

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2 
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4

console = Console()

def inicializa_banco():
        conexao = sqlite3.connect("track_jobs.db")
        cursor = conexao.cursor()

        cursor.execute(
            """create table if not exists empresas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            site TEXT,
            setor TEXT
            )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            link TEXT NOT NULL,
            data_aplicacao DATE,
            status TEXT DEFAULT 'em análise',
            detalhes TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY(idEmpresa) REFERENCES empresas(id)
            )"""
            )

        conexao.close()

def main():
    console.print(Panel("[bold magenta]TrackJobs - Gerenciador de Candidaturas[/bold magenta]", expand=False))

    inicializa_banco()

    msg_prompt = (
        "[bold cyan]Escolha uma opção abaixo:[/bold cyan]\n\n"
        "[green]1[/green] - Cadastrar Candidatura\n"
        "[green]2[/green] - Editar Status da Candidatura\n"
        "[green]3[/green] - Editar Candidatura\n"
        "[green]4[/green] - Remover Candidatura\n"
    )
    code = IntPrompt.ask(msg_prompt, choices=['1', '2', '3', '4'])

    if code == CADASTRAR_CANDIDATURA:
        pass
    elif code == EDITAR_STATUS:
        pass
    elif code == EDITAR_CANDIDATURA:
        pass
    else:
        pass

main()