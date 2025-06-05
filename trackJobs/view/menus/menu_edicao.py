import curses

from .menu import CANDIDATURA_SELECIONADA
from .menu import Menu
from .menu import MOVER_BAIXO
from .menu import MOVER_CIMA
from .menu import VOLTAR_MENU
from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException

CAMPOS_VAGA = ["nome", "link", "data_aplicacao", "status", "descricao"]


class MenuEdicao(Menu):
    def __init__(self, tela, controller: JobController):
        super().__init__(tela, controller=controller)
        self.index_campo_atual = 0

    def exibir_campo(self, campo, dados, i, campo_pra_print):
        _, largura = self.tela.getmaxyx()
        margem = 2  # Margem de segurança para evitar estouro
        if campo == "data_aplicacao":
            campo = "data de aplicação"
        elif campo == "descricao":
            campo = "descrição"

        if (
            campo_pra_print == self.index_campo_atual
        ):  # Se o cursor estiver no campo, mostra o valor
            msg = f"> {campo.capitalize()}: {dados}\n"
        else:
            msg = f"> {campo.capitalize()}\n"

        largura_disponivel = max(
            0, largura - margem * 2
        )  # Garante que não fique negativo
        msg_truncada = msg[
            : largura_disponivel + 3
        ]  # Corta a mensagem para caber na tela

        estilo = (
            curses.A_REVERSE
            if campo_pra_print == self.index_campo_atual
            else curses.A_NORMAL
        )
        self.tela.addstr(i + 2, 2, msg_truncada, estilo)

    def interpreta_teclado_menu_edicao(self):
        entrada_user = self.tela.getch()  # Aguarda entrada do teclado

        if (
            entrada_user == MOVER_BAIXO
            and self.index_campo_atual < len(CAMPOS_VAGA) - 1
        ):
            self.index_campo_atual += 1
        elif entrada_user == MOVER_CIMA and self.index_campo_atual > 0:
            self.index_campo_atual -= 1
        elif entrada_user == CANDIDATURA_SELECIONADA:
            self.tela.clear()
            return CAMPOS_VAGA[self.index_campo_atual]
        elif entrada_user == VOLTAR_MENU:
            self.tela.clear()
            raise RetornarMenuException

        return None

    def exibir_menu_edicao(
        self, candidatura: dict, itens_exibidos: int, posicao_scroll: int
    ):
        msg = (
            "Escolha o campo que queira editar da vaga escolhida abaixo:\n"
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)\n\n"
        )
        self.tela.addstr(0, 0, msg)

        self.index_candidatura_atual = self.index_campo_atual
        posicao_scroll = self.ajustar_scroll(posicao_scroll, itens_exibidos)

        for i, campo in enumerate(CAMPOS_VAGA):
            campo_pra_print = i + posicao_scroll
            self.exibir_campo(campo, candidatura[campo], i, campo_pra_print)

    def menu_edicao(self, candidatura: dict):
        curses.curs_set(0)  # Oculta o cursor no terminal
        self.tela.keypad(True)
        self.tela.clear()

        self.index_campo_atual = 0
        posicao_scroll = 0

        while True:
            max_linhas, _ = self.tela.getmaxyx()
            itens_exibidos = max_linhas - 5

            self.tela.clear()

            self.exibir_menu_edicao(candidatura, itens_exibidos, posicao_scroll)

            result = self.interpreta_teclado_menu_edicao()
            if result:
                return result

    def exibe_mensagem_sucesso(self, novo_status, campo_atualizado="Status"):
        if campo_atualizado == "Data_aplicaçao":
            campo_atualizado = "Data de aplicação"
        self.tela.clear()
        self.tela.addstr(
            5, 5, f"✅ Campo {campo_atualizado} atualizado com sucesso!", curses.A_BOLD
        )
        self.tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        self.tela.getch()  # Espera pressionar uma tecla
