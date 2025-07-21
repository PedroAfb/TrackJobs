import questionary
from rich.console import Console

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.exceptions import TrackJobsException
from trackJobs.view.menus.menu_edicao import MenuEdicao


class EdicaoCliView:
    def __init__(self, tela, controller: JobController):
        self.tela = tela
        self.controller = controller
        self.menu_edicao = MenuEdicao(tela, controller=controller)
        self.console = Console()

    def edicao(self):
        try:
            cand_selecionada = self.menu_edicao.escolha_candidatura()
            campo_selecionado = self.menu_edicao.menu_edicao(cand_selecionada)

            novo_dado = self._solicitar_novo_valor(campo_selecionado)

            self.controller.atualizar_candidatura(
                cand_selecionada, campo_selecionado, novo_dado
            )
            self.menu_edicao.exibe_mensagem_sucesso(
                None, campo_selecionado.capitalize()
            )
        except RetornarMenuException:
            pass
        except TrackJobsException as e:
            self.menu_edicao.exibe_mensagem_erro(str(e))

    def _solicitar_novo_valor(self, campo_selecionado: str) -> str:
        """Solicita novo valor para o campo com validação"""
        while True:
            novo_dado = (
                questionary.text(
                    "\nInforme o novo valor do campo "
                    f"{campo_selecionado.capitalize()}:\n"
                )
                .ask()
                .strip()
            )

            validacao = self.controller.validar_campo(campo_selecionado, novo_dado)

            if validacao is True:
                return novo_dado
            elif isinstance(validacao, str):
                # Usa Rich Console em vez de curses para erros
                self.console.print(f"[bold red]❌ {validacao}[/bold red]")
                self.console.print("[yellow]Tente novamente...[/yellow]\n")
