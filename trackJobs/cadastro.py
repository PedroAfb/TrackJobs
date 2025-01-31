import validators
from rich.prompt import Prompt
from rich.console import Console
import click
import sqlite3
from datetime import datetime

console = Console()

def obter_site_empresa(cursor):
    while True:
        site_empresa = Prompt.ask("Qual o site da empresa?[OPCIONAL]")

        if not site_empresa:
            return None
        elif validators.url(site_empresa):
            cursor.execute("SELECT 1 FROM empresas WHERE site = ?", (site_empresa,))
            if cursor.fetchone():
                raise sqlite3.IntegrityError("empresas.site")
            return site_empresa
        else:
            print("[bold red]URL inválida. Digite um link válido ou deixe em branco.[/bold red]")


def cadastra_candidatura():
    console.print("[bold magenta]\nCadastro[/bold magenta]\n")

    nome = click.prompt("Qual o nome da vaga?[OBRIGATÓRIO]")
    nome = nome.strip().lower()

    link = click.prompt("Qual o link da vaga?[OBRIGATÓRIO]") # tem que ser unique
    status = Prompt.ask(
        "Qual o status da candidatura?[OPCIONAL]",
        choices=["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"],
        default="candidatar-se",
        show_default=False)
    descricao = Prompt.ask("Coloque descrição sobre a vaga[OPCIONAL]")
    nome_empresa = Prompt.ask("Qual o nome da empresa?[OPCIONAL]")
    nome_empresa = nome_empresa.strip().lower()

    try:
        conexao = sqlite3.connect("track_jobs.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT 1 FROM empresas WHERE nome = ?", (nome_empresa,))
        empresa_existe = cursor.fetchone()
        

        if nome_empresa and not empresa_existe:    # Se o usuário escreveu no campo empresa e ela não está no banco de dados, o cadastro da empresa é realizado
            site_empresa = obter_site_empresa(cursor)
            setor_empresa = Prompt.ask("Qual o setor da empresa?[OPCIONAL]")
        
            cursor.execute(f"""
                INSERT INTO empresas (nome, site, setor) VALUES
                ('{nome_empresa}', '{site_empresa}', '{setor_empresa}')
                """)
            conexao.commit()

        if nome_empresa:    # Adiciona vaga com uma empresa associada
            id_empresa = cursor.execute("SELECT id FROM empresas WHERE nome = ?", (nome_empresa,)).fetchall()[0][0]
            msg_insert = (
                "INSERT INTO vagas (nome, link, status, descricao, idEmpresa) VALUES\n"
                f"('{nome}', '{link}', '{status}', '{descricao}', '{id_empresa}')"
            )
        else:
            msg_insert = (
            "INSERT INTO vagas (nome, link, status, descricao) VALUES\n"
            f"('{nome}', '{link}', '{status}', '{descricao}')"
            )

        cursor.execute(msg_insert)
        conexao.commit()
        console.print("[bold green]\nCadastro realizado com sucesso!\n[/bold green]")
        conexao.close()

    except sqlite3.IntegrityError as e:
        conexao.close()
        erro_duplicado = str(e)
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {erro_duplicado}")
        erro_duplicado = erro_duplicado.split(" ")[-1]
        console.print(
            f"[bold red]Erro ao cadastrar no banco de dados: {erro_duplicado} já foi cadastrada![/bold red]"
        )
        cadastra_candidatura()

    except Exception as e:
        conexao.close()
        console.print("[bold red]Erro inesperado ao cadastrar a vaga.[/bold red]")
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {str(e)}")
        cadastra_candidatura()