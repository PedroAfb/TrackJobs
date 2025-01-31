from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.panel import Panel
import click
import sqlite3
from exceptions import InicializacaoBancoException, CadastroBancoException
import validators

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
            link TEXT NOT NULL,
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

def cadastra_candidatura():
    nome = click.prompt("Qual o nome da vaga?[OBRIGATÓRIO]")
    link = click.prompt("Qual o link da vaga?[OBRIGATÓRIO]") # tem que ser unique
    data = Prompt.ask("Qual foi a data de aplicação?[OPCIONAL]")
    status = Prompt.ask(
        "Qual o status da candidatura?[OPCIONAL]",
        choices=["em análise", "entrevista", "rejeitado", "aceito"],
        default="em análise",
        show_default=False)
    descricao = Prompt.ask("Coloque descrição sobre a vaga[OPCIONAL]")
    nome_empresa = Prompt.ask("Qual o nome da empresa?[OPCIONAL]")

    try:
        conexao = sqlite3.connect("track_jobs.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT 1 FROM empresas WHERE nome = ?", (nome_empresa,))
        empresa_existe = cursor.fetchone()
        

        if nome_empresa and not empresa_existe:    # Se o usuário escreveu no campo empresa e ela não está no banco de dados, o cadastro da empresa é realizado
            site_empresa = Prompt.ask("Qual o site da empresa?[OPCIONAL]")
            setor_empresa = Prompt.ask("Qual o setor da empresa?[OPCIONAL]")
        
            cursor.execute(f"""
                INSERT INTO empresas (nome, site, setor) VALUES
                ('{nome_empresa}', '{site_empresa}', '{setor_empresa}')
                """)
            conexao.commit()

        if nome_empresa:    # Adiciona vaga com uma empresa associada
            id_empresa = cursor.execute("SELECT id FROM empresas WHERE nome = ?", (nome_empresa,)).fetchall()[0][0]
            msg_insert = (
                "INSERT INTO vagas (nome, link, data_aplicacao, status, descricao, idEmpresa) VALUES\n"
                f"('{nome}', '{link}', '{data}', '{status}', '{descricao}', '{id_empresa}')"
            )
        else:
            msg_insert = (
            "INSERT INTO vagas (nome, link, data_aplicacao, status, descricao) VALUES\n"
            f"('{nome}', '{link}', '{data}', '{status}', '{descricao}')"
            )

        cursor.execute(msg_insert)
        conexao.commit()
        console.print("[bold green]Cadastro realizado com sucesso![/bold green]")
        conexao.close()

    except sqlite3.IntegrityError as e:
        conexao.close()
        console.print(
            "[bold red]Erro ao cadastrar no banco de dados: Informação duplicada.[/bold red]"
        )
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {str(e)}")
        cadastra_candidatura()

    except Exception as e:
        conexao.close()
        console.print("[bold red]Erro inesperado ao cadastrar a vaga.[/bold red]")
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {str(e)}")
        cadastra_candidatura()


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