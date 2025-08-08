from rich.console import Console

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.view.menus.menu_visualizacao import MenuVisualizacao


class VisualizacaoCliView:
    """Classe responsável por exibir a visualização CLI."""

    def __init__(self, tela, controller: JobController):
        self.tela = tela
        self.controller = controller
        self.menu_visualizacao = MenuVisualizacao(tela, controller)
        self.console = Console()

    def visualizacao_candidatura(self):
        try:
            while True:
                cand_selecionada = self.menu_visualizacao.escolha_candidatura()
                cand_selecionada = self.controller.obter_dados_vaga(
                    cand_selecionada["link"]
                )
                self.menu_visualizacao.menu_da_candidatura(cand_selecionada)

        except RetornarMenuException:
            pass

        except Exception as e:
            self.menu_visualizacao.exibe_mensagem_erro(e)
