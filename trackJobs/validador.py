from datetime import date

import validators
from rich.console import Console

from trackJobs.banco_de_dados import BancoDeDados


def valida_nome(nome: str, console: Console):
    if not nome:
        console.print("[bold red]Nome não pode estar vazio.[/bold red]")
        return False

    return True


def valida_link(db_path: str, link: str, console: Console):
    if validators.url(link):
        db = BancoDeDados(db_path)
        db.cursor.execute("SELECT 1 FROM vagas WHERE link = ?", (link,))
        if not db.cursor.fetchone():
            return True

        msg = (
            "[bold red]Essa URL já foi cadastrada. [/bold red]"
            "[bold red]Digite um link válido.\n[/bold red]"
            "[bold magenta]Caso queira retornar ao menu principal[/bold magenta]"
            "[bold magenta], digite 6[/bold magenta]"
        )
        console.print(msg)
        return False

    else:
        console.print("[bold red]URL inválida. Digite um link válido.\n[/bold red]")
        return False


def valida_status(status: str, console: Console):
    status = status.strip().lower()
    if status not in [
        "candidatar-se",
        "em análise",
        "entrevista",
        "rejeitado",
        "aceito",
    ]:
        console.print(
            "[bold red]Status inválido. "
            "Digite um status entre candidatar-se, "
            "em análise, entrevista, rejeitado ou aceito.[/bold red]"
        )
        return False

    return True


def valida_data_aplicacao(data: str, console: Console):
    if not data:
        return True
    try:
        date.fromisoformat(data)
        return True
    except ValueError:
        console.print(
            "[bold red]Data inválida. Digite uma [/bold red]"
            "[bold red]data válida (YYYY-MM-DD) ou deixe em branco.[/bold red]"
        )
        return False


def valida_descricao(descricao: str, console: Console):
    return True


VALIDADORES = {
    "nome": lambda db_path, novo_dado, console: valida_nome(novo_dado, console),
    "link": lambda db_path, novo_dado, console: valida_link(
        db_path, novo_dado, console
    ),
    "status": lambda db_path, novo_dado, console: valida_status(novo_dado, console),
    "descriçao": lambda db_path, novo_dado, console: valida_descricao(
        novo_dado, console
    ),
    "data_aplicaçao": lambda db_path, novo_dado, console: valida_data_aplicacao(
        novo_dado, console
    ),
    "nome_empresa": lambda db_path, novo_dado, console: valida_nome(novo_dado, console),
    "site_empresa": lambda db_path, novo_dado, console: valida_link(
        db_path, novo_dado, console
    ),
    "setor_empresa": lambda db_path, novo_dado, console: valida_nome(
        novo_dado, console
    ),
}
