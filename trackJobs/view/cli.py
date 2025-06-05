import questionary
from rich.console import Console
from rich.panel import Panel

from .cadastro_cli import CadastroCliView
from trackJobs.controller.job_controller import JobController
from trackJobs.utils import CUSTOM_STYLE
from trackJobs.view.edicao_cli import EdicaoCliView


class CliView:
    def __init__(self, controller: JobController, tela) -> None:
        self.controller = controller
        self.tela = tela
        self.console = Console()

    def menu_principal(self) -> None:
        """Exibe o menu principal da ferramenta"""
        while True:
            self.console.print(
                Panel(
                    "[bold magenta]TrackJobs - "
                    "Gerenciador de Candidaturas[/bold magenta]",
                    expand=False,
                )
            )

            opcao = questionary.select(
                "Escolha uma opção abaixo:\n",
                choices=[
                    "Cadastrar Candidatura",
                    "Visualizar Candidaturas",
                    "Editar Status da Candidatura",
                    "Editar Candidatura",
                    "Remover Candidatura",
                    "Fechar Ferramenta",
                ],
                style=CUSTOM_STYLE,
            ).ask()

            if opcao == "Cadastrar Candidatura":
                CadastroCliView(self.controller, self.tela).cadastro()
            elif opcao == "Visualizar Candidaturas":
                self.visualizacao()
            elif opcao == "Editar Status da Candidatura":
                self.edita_status()
            elif opcao == "Editar Candidatura":
                EdicaoCliView(self.tela, self.controller).edicao()
            elif opcao == "Remover Candidatura":
                self.remocao()
            else:
                break
