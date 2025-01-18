from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.panel import Panel
import datetime
import click
import sqlite3

CADASTRAR_CANDIDATURA = 1
EDITAR_STATUS = 2 
EDITAR_CANDIDATURA = 3
REMOVER_CANDIDATURA = 4
DATA_NULA = '0/0/0'

console = Console()

def inicializa_banco():
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
            link TEXT NOT NULL,
            data_aplicacao DATE,
            status TEXT DEFAULT 'em análise',
            detalhes TEXT,
            idEmpresa INTEGER,
            FOREIGN KEY(idEmpresa) REFERENCES empresas(id)
            )"""
            )

        conexao.close()

def cadastra_candidatura():
    nome = click.prompt("Qual o nome da vaga?[OBRIGATÓRIO]")
    link = click.prompt("Qual o link da vaga?[OBRIGATÓRIO]")
    data = Prompt.ask("Qual foi a data de aplicação?[OPCIONAL]")
    status = Prompt.ask(
        "Qual o status da candidatura?[OPCIONAL]",
        choices=["em análise", "entrevista", "rejeitado", "aceito"],
        default="em análise",
        show_default=False)
    detalhes = Prompt.ask("Coloque detalhes sobre a vaga[OPCIONAL]")
    nome_empresa = Prompt.ask("Qual o nome da empresa?[OPCIONAL]")

    conexao = sqlite3.connect("track_jobs.db")
    cursor = conexao.cursor()

    lista_empresas = cursor.execute("""select nome from empresas""").fetchall()
    print(lista_empresas)

    if nome_empresa and nome_empresa not in lista_empresas:
        site_empresa = Prompt.ask("Qual o site da empresa?[OPCIONAL]")
        setor_empresa = Prompt.ask("Qual o setor da empresa?[OPCIONAL]")
    
        cursor.execute(f"""
            INSERT INTO empresas (nome, site, setor) VALUES
            ('{nome_empresa}', '{site_empresa}', '{setor_empresa}')
            """)
        conexao.commit()


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
    opcao = IntPrompt.ask(msg_prompt, choices=['1', '2', '3', '4'])

    if opcao == CADASTRAR_CANDIDATURA:
        cadastra_candidatura()
    elif opcao == EDITAR_STATUS:
        pass
    elif opcao == EDITAR_CANDIDATURA:
        pass
    else:
        pass

main()