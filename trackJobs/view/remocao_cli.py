import questionary
from rich.console import Console

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.view.menus.menu_remocao import MenuRemocao


class RemocaoCliView:
    def __init__(self, tela, controller: JobController):
        self.tela = tela
        self.controller = controller
        self.menu_remocao = MenuRemocao(tela, controller=controller)
        self.console = Console()

    def remocao(self):
        try:
            certeza = False
            while not certeza:
                cand_selecionada = self.menu_remocao.escolha_candidatura()
                certeza = questionary.confirm(
                    f"Tem certeza que deseja remover a candidatura "
                    f"{cand_selecionada['nome']}?"
                ).ask()

            self.controller.remover_candidatura(cand_selecionada)

            self.menu_remocao.tela.clear()
            self.menu_remocao.exibe_mensagem_sucesso(None)

        except RetornarMenuException:
            pass

        except Exception as e:
            self.menu_remocao.exibe_mensagem_erro(e)
