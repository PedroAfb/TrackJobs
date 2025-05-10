import questionary
from rich.console import Console

from .exceptions import RetornarMenuException
from .menu import Menu
from .utils import realiza_update

console = Console()

OPCOES_STATUS = ["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"]


class MenuStatus(Menu):
    def __init__(self, tela, db_path="track_jobs.db"):
        super().__init__(tela, db_path=db_path)

    def menu_status(self, candidatura):
        novo_status = questionary.select(
            f"\n\n\nEditar status da candidatura {candidatura['nome']} para:",
            choices=OPCOES_STATUS,
        ).ask()

        return novo_status


def edita_status(tela, db_path="track_jobs.db"):
    try:
        menu = MenuStatus(tela, db_path)
        cand_selecionada = menu.escolha_candidatura()
        novo_status = menu.menu_status(cand_selecionada)
        realiza_update(menu.db, cand_selecionada, "status", novo_status)

        menu.exibe_mensagem_sucesso(novo_status)

    except RetornarMenuException:
        pass

    except Exception as e:
        menu.exibe_mensagem_erro(e)
