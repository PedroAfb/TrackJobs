import sqlite3
from sqlite3 import Connection
from sqlite3 import Cursor

import click
import validators
from rich.console import Console
from rich.prompt import Prompt

from .exceptions import RetornarMenuException

console = Console()
VOLTAR_MENU = 6


def obter_site_empresa(cursor: Cursor):
    while True:
        site_empresa = Prompt.ask("Qual o site da empresa?[OPCIONAL]")

        if not site_empresa:
            return None
        elif validators.url(site_empresa):
            cursor.execute("SELECT 1 FROM empresas WHERE site = ?", (site_empresa,))
            if not cursor.fetchone():
                return site_empresa
            msg = (
                "[bold red]Essa URL já foi cadastrada.[/bold red]"
                "[bold red] Digite um link válido ou deixe em branco.[/bold red]"
            )
            console.print(msg)

        else:
            msg = (
                "[bold red]URL inválida. [/bold red]"
                "[bold red]Digite um link válido ou deixe em branco.[/bold red]"
            )
            console.print(msg)


def obter_link_vaga(db_path="track_jobs.db"):
    link = None
    while link != "6":
        link = Prompt.ask("Qual o link da vaga?[OBRIGATÓRIO]")

        if validators.url(link):
            conexao = sqlite3.connect(db_path)
            cursor = conexao.cursor()
            cursor.execute("SELECT 1 FROM vagas WHERE link = ?", (link,))

            if not cursor.fetchone():
                return link
            msg = (
                "[bold red]Essa URL já foi cadastrada. [/bold red]"
                "[bold red]Digite um link válido.[/bold red]"
            )
            console.print(msg)
            console.print("Caso queira retornar ao menu principal, digite 6")

            conexao.close()
        else:
            console.print("[bold red]URL inválida. Digite um link válido.[/bold red]")
            console.print("Caso queira retornar ao menu principal, digite 6")

    raise RetornarMenuException


def verifica_empresa_sql(cursor: Cursor, nome_empresa: str):
    cursor.execute("SELECT 1 FROM empresas WHERE nome = ?", (nome_empresa,))
    return cursor.fetchone()


def coleta_dados_vaga():
    dados_candidatura = dict()

    nome = click.prompt(
        "Qual o nome da vaga?[OBRIGATÓRIO]\n" "Caso queira retornar ao menu, digite 6"
    )
    dados_candidatura["nome"] = nome.strip().lower()

    dados_candidatura["link"] = obter_link_vaga()
    dados_candidatura["status"] = Prompt.ask(
        "Qual o status da candidatura?[OPCIONAL]",
        choices=["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"],
        default="candidatar-se",
        show_default=False,
    )
    dados_candidatura["descricao"] = Prompt.ask(
        "Coloque descrição sobre a vaga[OPCIONAL]"
    )
    nome_empresa = Prompt.ask("Qual o nome da empresa?[OPCIONAL]")
    dados_candidatura["nome_empresa"] = nome_empresa.strip().lower()

    return dados_candidatura


def coleta_dados_empresa(cursor: Cursor):
    site_empresa = obter_site_empresa(cursor)
    setor_empresa = Prompt.ask("Qual o setor da empresa?[OPCIONAL]")
    return site_empresa, setor_empresa


def cadastra_empresa(conexao: Connection, cursor: Cursor, nome_empresa: str):
    site_empresa, setor_empresa = coleta_dados_empresa(cursor)

    msg_insert_empresas = f"""
        INSERT INTO empresas (nome, site, setor) VALUES
        ('{nome_empresa}', '{site_empresa}', '{setor_empresa}')
        """
    cursor.execute(msg_insert_empresas)
    conexao.commit()

    console.print(
        "[bold green]\nCadastro da empresa realizado com sucesso!\n[/bold green]"
    )


def cadastra_vaga(conexao: Connection, cursor: Cursor, dados_candidatura: dict):
    if dados_candidatura["nome_empresa"]:  # Adiciona vaga com uma empresa associada
        id_empresa = cursor.execute(
            "SELECT id FROM empresas WHERE nome = ?",
            (dados_candidatura["nome_empresa"],),
        ).fetchall()[0][0]
        msg_insert_vagas = (
            "INSERT INTO vagas "
            "(nome, link, status, descricao, idEmpresa) VALUES\n"
            f"('{dados_candidatura['nome']}', '{dados_candidatura['link']}', "
            f"'{dados_candidatura['status']}', "
            f"'{dados_candidatura['descricao']}', '{id_empresa}')"
        )
    else:
        msg_insert_vagas = (
            "INSERT INTO vagas "
            "(nome, link, status, descricao) VALUES\n"
            f"('{dados_candidatura['nome']}', '{dados_candidatura['link']}', "
            f"'{dados_candidatura['status']}', '{dados_candidatura['descricao']}')"
        )

    cursor.execute(msg_insert_vagas)
    conexao.commit()


def cadastra_candidatura(db_path="track_jobs.db", teste=False):
    console.print("[bold magenta]\nCadastro[/bold magenta]\n")

    try:
        dados_candidatura = coleta_dados_vaga()

        conexao = sqlite3.connect(db_path)
        cursor = conexao.cursor()

        nome_empresa = dados_candidatura["nome_empresa"]
        empresa_existe = verifica_empresa_sql(cursor, nome_empresa)

        if nome_empresa and not empresa_existe:
            cadastra_empresa(conexao, cursor, nome_empresa)

        cadastra_vaga(conexao, cursor, dados_candidatura)

        console.print(
            "[bold green]\nCadastro da vaga realizado com sucesso!\n[/bold green]"
        )
        conexao.close()

    except RetornarMenuException:
        pass

    except sqlite3.IntegrityError as e:
        conexao.close()
        erro_duplicado = str(e)
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {erro_duplicado}")
        campo_duplicado = erro_duplicado.split(" ")[-1]
        msg = (
            "[bold red]Erro ao cadastrar no banco de dados: [/bold red]"
            f"[bold red]{campo_duplicado} já foi cadastrada![/bold red]"
        )
        console.print(msg)
        if teste:
            raise e
        cadastra_candidatura()

    except Exception as e:
        conexao.close()
        console.print("[bold red]Erro inesperado ao cadastrar a vaga.[/bold red]")
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {str(e)}")
        cadastra_candidatura()
