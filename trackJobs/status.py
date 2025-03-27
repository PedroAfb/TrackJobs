import questionary
from rich.console import Console

from .exceptions import RetornarMenuException
from .menu import FILTROS
from .menu import Menu
from .utils import filtra_candidaturas
from .utils import realiza_update

console = Console()

OPCOES_STATUS = ["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"]


class MenuStatus(Menu):
    def __init__(self, tela):
        super().__init__(tela)

    def menu_status(self, candidatura):
        novo_status = questionary.select(
            f"\n\n\nEditar status da candidatura {candidatura['nome']} para:",
            choices=OPCOES_STATUS,
        ).ask()

        return novo_status


def edita_status(tela, db_path="track_jobs.db"):
    try:
        menu = MenuStatus(tela)
        index_candidatura = "nenhum"

        while index_candidatura in FILTROS.keys():
            candidaturas = filtra_candidaturas(db_path, index_candidatura)
            index_candidatura = menu.menu_candidaturas(candidaturas)

        # Seleciona a candidatura e atualiza o status
        cand_selecionada = candidaturas[index_candidatura]
        novo_status = menu.menu_status(cand_selecionada)
        realiza_update(db_path, cand_selecionada, "status", novo_status)

        menu.exibe_mensagem_sucesso(novo_status)

    except RetornarMenuException:
        pass

    except Exception as e:
        menu.exibe_mensagem_erro(e)
