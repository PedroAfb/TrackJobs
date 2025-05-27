from datetime import date

import validators
from rich.console import Console

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.cadastro import verifica_empresa_sql
from trackJobs.exceptions import CampoDuplicadoException
from trackJobs.exceptions import DataInvalidaException
from trackJobs.exceptions import NomeVazioException
from trackJobs.exceptions import StatusInvalidoException
from trackJobs.exceptions import URLInvalidaException
from trackJobs.exceptions import URLJaCadastradaException


def valida_nome(nome: str, console: Console):
    if not nome:
        raise NomeVazioException()

    return True


def valida_nome_empresa(db: BancoDeDados, nome_empresa: str, console: Console):
    if not nome_empresa:
        raise NomeVazioException()

    empresa_existe = verifica_empresa_sql(db, nome_empresa)
    if empresa_existe:
        raise CampoDuplicadoException("Empresa já cadastrada.")

    return True


def valida_link(db: BancoDeDados, link: str, console: Console):
    if not link:
        raise

    elif validators.url(link):
        db.cursor.execute("SELECT 1 FROM vagas WHERE link = ?", (link,))
        if not db.cursor.fetchone():
            return True

        raise URLJaCadastradaException()

    else:
        raise URLInvalidaException()


def valida_link_empresa(db: BancoDeDados, link: str, console: Console):
    if not link:
        return True

    elif validators.url(link):
        db.cursor.execute("SELECT 1 FROM empresas WHERE site = ?", (link,))
        if not db.cursor.fetchone():
            return True

        raise URLJaCadastradaException()

    raise URLInvalidaException()


def valida_status(status: str, console: Console):
    status = status.strip().lower()
    if status not in [
        "candidatar-se",
        "em análise",
        "entrevista",
        "rejeitado",
        "aceito",
    ]:
        raise StatusInvalidoException()

    return True


def valida_data_aplicacao(data: str, console: Console):
    if not data:
        return True
    try:
        date.fromisoformat(data)
        return True
    except ValueError:
        raise DataInvalidaException()


VALIDADORES = {
    "nome": lambda db, novo_dado, console: valida_nome(novo_dado, console),
    "link": lambda db, novo_dado, console: valida_link(db, novo_dado, console),
    "status": lambda db, novo_dado, console: valida_status(novo_dado, console),
    "descriçao": lambda db, novo_dado, console: True,
    "data_aplicaçao": lambda db, novo_dado, console: valida_data_aplicacao(
        novo_dado, console
    ),
    "nome_empresa": lambda db, novo_dado, console: valida_nome_empresa(
        db, novo_dado, console
    ),
    "site_empresa": lambda db, novo_dado, console: valida_link_empresa(
        db, novo_dado, console
    ),
    "setor_empresa": lambda db, novo_dado, console: True,
}
