import sqlite3
from datetime import date
from sqlite3 import Connection
from sqlite3 import Cursor

import click
import validators
from rich.console import Console
from rich.prompt import Prompt

from .exceptions import RetornarMenuException

console = Console()
VOLTAR_MENU = "6"


def verificar_saida(valor):
    """Verifica se o usuário deseja retornar ao menu."""
    if valor.strip() == VOLTAR_MENU:
        raise RetornarMenuException


def obter_site_empresa(cursor_db: Cursor):
    while True:
        site_empresa = Prompt.ask("Qual o site da empresa?[OPCIONAL]")

        if not site_empresa:
            return None
        elif validators.url(site_empresa):
            cursor_db.execute("SELECT 1 FROM empresas WHERE site = ?", (site_empresa,))
            if not cursor_db.fetchone():
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
    while link != VOLTAR_MENU:
        link = Prompt.ask("Qual o link da vaga?[OBRIGATÓRIO]")

        if validators.url(link):
            conexao_db = sqlite3.connect(db_path)
            cursor_db = conexao_db.cursor()
            cursor_db.execute("SELECT 1 FROM vagas WHERE link = ?", (link,))

            if not cursor_db.fetchone():
                return link

            msg = (
                "[bold red]Essa URL já foi cadastrada. [/bold red]"
                "[bold red]Digite um link válido.\n[/bold red]"
                "[bold magenta]Caso queira retornar ao menu principal[/bold magenta]"
                "[bold magenta], digite 6[/bold magenta]"
            )
            console.print(msg)

            conexao_db.close()
        else:
            msg = (
                "[bold red]URL inválida. Digite um link válido.\n[/bold red]"
                "[bold magenta]Caso queira retornar ao menu principal[/bold magenta]"
                "[bold magenta], digite 6[/bold magenta]"
            )
            console.print(msg)

    raise RetornarMenuException


def verifica_empresa_sql(cursor_db: Cursor, nome_empresa: str):
    cursor_db.execute("SELECT 1 FROM empresas WHERE nome = ?", (nome_empresa,))
    return cursor_db.fetchone()


def obter_data_candidatura():
    while True:
        data_candidatura = Prompt.ask(
            "Qual a data da candidatura (YYYY-MM-DD)?[OPCIONAL]",
        )
        if not data_candidatura:
            return None
        verificar_saida(data_candidatura)
        try:
            date.fromisoformat(data_candidatura)
            return data_candidatura
        except ValueError:
            console.print(
                "[bold red]Data inválida. Digite uma [/bold red]"
                "[bold red]data válida (YYYY-MM-DD) ou deixe em branco.[/bold red]"
            )


def coleta_dados_vaga():
    dados_candidatura = dict()

    nome = click.prompt("Qual o nome da vaga?[OBRIGATÓRIO]\n")
    verificar_saida(nome)
    dados_candidatura["nome"] = nome.strip().lower()

    dados_candidatura["link"] = obter_link_vaga()

    status = Prompt.ask(
        "Qual o status da candidatura?[OPCIONAL]",
        choices=[
            "candidatar-se",
            "em análise",
            "entrevista",
            "rejeitado",
            "aceito",
            "6",
        ],
        default="candidatar-se",
        show_default=False,
    )
    verificar_saida(status)
    dados_candidatura["status"] = status

    dados_candidatura["data_aplicacao"] = obter_data_candidatura()

    descricao = Prompt.ask("Coloque descrição sobre a vaga[OPCIONAL]")
    verificar_saida(descricao)
    dados_candidatura["descricao"] = descricao

    nome_empresa = Prompt.ask("Qual o nome da empresa?[OPCIONAL]")
    verificar_saida(nome_empresa)
    dados_candidatura["nome_empresa"] = nome_empresa.strip().lower()

    return dados_candidatura


def coleta_dados_empresa(cursor_db: Cursor):
    site_empresa = obter_site_empresa(cursor_db)
    setor_empresa = Prompt.ask("Qual o setor da empresa?[OPCIONAL]")
    return site_empresa, setor_empresa


def cadastra_empresa(conexao_db: Connection, cursor_db: Cursor, nome_empresa: str):
    site_empresa, setor_empresa = coleta_dados_empresa(cursor_db)

    msg_insert_empresas = """
        INSERT INTO empresas (nome, site, setor) VALUES
        (?, ?, ?)
        """
    cursor_db.execute(
        msg_insert_empresas,
        (
            nome_empresa,
            site_empresa,
            setor_empresa,
        ),
    )
    conexao_db.commit()

    console.print(
        "[bold green]\nCadastro da empresa realizado com sucesso!\n[/bold green]"
    )


def cadastra_vaga(conexao_db: Connection, cursor_db: Cursor, dados_candidatura: dict):
    if dados_candidatura["nome_empresa"]:  # Adiciona vaga com uma empresa associada
        id_empresa = cursor_db.execute(
            "SELECT id FROM empresas WHERE nome = ?",
            (dados_candidatura["nome_empresa"],),
        ).fetchall()[0][0]
        msg_insert_vagas = """INSERT INTO vagas
            (nome, link, status, descriçao, data_aplicaçao, idEmpresa) VALUES
            (?, ?, ?, ?, ?, ?)"""
        params = (
            dados_candidatura["nome"],
            dados_candidatura["link"],
            dados_candidatura["status"],
            dados_candidatura["descricao"],
            dados_candidatura["data_aplicacao"],
            id_empresa,
        )

    else:
        msg_insert_vagas = """INSERT INTO vagas
            (nome, link, status, descriçao, data_aplicaçao) VALUES
            (?, ?, ?, ?, ?)"""
        params = (
            dados_candidatura["nome"],
            dados_candidatura["link"],
            dados_candidatura["status"],
            dados_candidatura["descricao"],
            dados_candidatura["data_aplicacao"],
        )

    cursor_db.execute(msg_insert_vagas, params)
    conexao_db.commit()


def cadastra_candidatura(db_path="track_jobs.db", teste=False):
    console.print("[bold magenta]\nCadastro[/bold magenta]\n")
    console.print(
        "[bold magenta]Caso queira retornar ao menu, digite 6[/bold magenta]\n"
    )

    try:
        dados_candidatura = coleta_dados_vaga()

        conexao_db = sqlite3.connect(db_path)
        cursor_db = conexao_db.cursor()

        nome_empresa = dados_candidatura["nome_empresa"]
        empresa_existe = verifica_empresa_sql(cursor_db, nome_empresa)

        if nome_empresa and not empresa_existe:
            cadastra_empresa(conexao_db, cursor_db, nome_empresa)

        cadastra_vaga(conexao_db, cursor_db, dados_candidatura)

        console.print(
            "[bold green]\nCadastro da vaga realizado com sucesso!\n[/bold green]"
        )
        conexao_db.close()

    except RetornarMenuException:
        pass

    except sqlite3.IntegrityError as e:
        conexao_db.close()
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
        conexao_db.close()
        console.print("[bold red]Erro inesperado ao cadastrar a vaga.[/bold red]")
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {str(e)}")
        cadastra_candidatura()
