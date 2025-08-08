import curses

from trackJobs.controller.job_controller import JobController
from trackJobs.view.menus.menu import Menu


class MenuRemocao(Menu):
    def __init__(self, tela, controller: JobController):
        msg_menu = (
            "Selecione uma candidatura para remover "
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)"
        )
        super().__init__(
            tela,
            controller,
            msg_menu,
        )

    def exibe_mensagem_sucesso(self, novo_status, campo_atualizado="Status"):
        self.tela.clear()
        self.tela.addstr(5, 5, "✅ Candidatura removida com sucesso!", curses.A_BOLD)
        self.tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        self.tela.getch()
