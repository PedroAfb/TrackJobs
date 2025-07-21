from rich.console import Console

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.view.menus.menu_status import MenuStatus


class StatusCliView:
    def __init__(self, tela, controller: JobController):
        self.tela = tela
        self.controller = controller
        self.menu_status = MenuStatus(tela, controller=controller)
        self.console = Console()

    def edita_status(self):
        try:
            cand_selecionada = self.menu_status.escolha_candidatura()
            novo_status = self.menu_status.menu_status(cand_selecionada)
            self.controller.atualizar_candidatura(
                cand_selecionada, "status", novo_status
            )

            self.menu_status.exibe_mensagem_sucesso(novo_status)

        except RetornarMenuException:
            pass

        except Exception as e:
            self.menu_status.exibe_mensagem_erro(e)
