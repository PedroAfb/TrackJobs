import curses

import questionary

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException

FILTROS = {"limpa_filtro": 0, "nome": 1, "link": 2, "status": 3, "nenhum": -1}
MOVER_BAIXO = curses.KEY_DOWN
MOVER_CIMA = curses.KEY_UP
CANDIDATURA_SELECIONADA = 10
VOLTAR_MENU = 27
MENU_VAZIO = 4


class Menu:
    def __init__(self, tela, controller: JobController, msg_menu: str = ""):
        self.tela = tela
        self.index_candidatura_atual = 0
        self.controller = controller
        if msg_menu:
            self.msg_menu = msg_menu
        else:
            self.msg_menu = (
                "Selecione uma candidatura para editar "
                "(Setas para navegar, Enter para selecionar "
                "e ESC para retornar ao menu principal)"
            )

    def ajustar_scroll(self, posicao_scroll, itens_exibidos):
        """
        Ajusta a posição do scroll para manter o item selecionado visível.
        """
        if self.index_candidatura_atual < posicao_scroll:
            return self.index_candidatura_atual
        elif self.index_candidatura_atual >= posicao_scroll + itens_exibidos:
            return self.index_candidatura_atual - itens_exibidos + 1
        return posicao_scroll

    def exibir_item(self, c, i, cand_pra_print):
        """
        Exibe o menu com as candidaturas e opções de filtro.
        """
        if type(c) is str:
            estilo = (
                curses.A_BOLD | curses.A_REVERSE
                if cand_pra_print == self.index_candidatura_atual
                else curses.A_BOLD
            )
            self.tela.addstr(i + 2, 2, f"> {c}", estilo)  # Printa os filtros
        else:
            estilo = (
                curses.A_REVERSE
                if cand_pra_print == self.index_candidatura_atual
                else curses.A_NORMAL
            )
            self.tela.addstr(
                i + 2, 2, f"  {c['nome']} - {c['status']}", estilo
            )  # Printa as candidaturas

    def exibir_menu(self, opcoes_menu, posicao_scroll, itens_exibidos):
        """
        Exibe o menu com as candidaturas e opções de filtro.
        """
        self.tela.clear()
        max_linhas, _ = self.tela.getmaxyx()
        self.tela.addstr(0, 0, self.msg_menu)

        posicao_scroll = self.ajustar_scroll(posicao_scroll, itens_exibidos)

        for i in range(itens_exibidos):
            cand_pra_print = i + posicao_scroll
            if cand_pra_print >= len(opcoes_menu):
                break

            c = opcoes_menu[cand_pra_print]
            self.exibir_item(c, i, cand_pra_print)

        # Exibe o link da candidatura selecionada no rodapé, se aplicável
        if type(opcoes_menu[self.index_candidatura_atual]) is not str:
            self.exibir_link(max_linhas, opcoes_menu[self.index_candidatura_atual])

        if len(opcoes_menu) == MENU_VAZIO:
            self.tela.addstr(i + 2, 2, "Nenhuma candidatura encontrada", curses.A_BOLD)

    def exibir_link(self, max_linhas, candidatura):
        """
        Exibe o link da candidatura selecionada.
        """
        self.tela.addstr(
            max_linhas - 2, 2, "📎 Link da vaga selecionada: ", curses.A_BOLD
        )
        self.tela.addstr(
            max_linhas - 2,
            31,
            candidatura["link"],
            curses.A_UNDERLINE,
        )

    def interpreta_teclado(self, opcoes_menu):
        entrada_user = self.tela.getch()  # Aguarda entrada do teclado

        # Movimentação da seleção para cima e para baixo
        if (
            entrada_user == MOVER_BAIXO
            and self.index_candidatura_atual < len(opcoes_menu) - 1
        ):
            self.index_candidatura_atual += 1
        elif entrada_user == MOVER_CIMA and self.index_candidatura_atual > 0:
            self.index_candidatura_atual -= 1
        elif entrada_user == CANDIDATURA_SELECIONADA:
            self.tela.clear()
            if self.index_candidatura_atual < MENU_VAZIO:
                return next(  # Retorna o filtro selecionado
                    (
                        chave
                        for chave, valor in FILTROS.items()
                        if valor == self.index_candidatura_atual
                    ),
                    None,
                )
            else:
                return self.index_candidatura_atual - MENU_VAZIO
        elif entrada_user == VOLTAR_MENU:
            self.tela.clear()
            raise RetornarMenuException

        return None

    def menu_candidaturas(self, opcoes_menu: list):
        """
        Exibe o menu principal de candidaturas e
        permite ao usuário navegar e selecionar.
        """
        opcoes_menu = [
            "Limpar filtro",
            "Filtrar por nome",
            "Filtrar por link",
            "Filtrar por status",
        ] + opcoes_menu

        curses.curs_set(0)  # Oculta o cursor no terminal
        self.tela.keypad(True)
        self.tela.clear()

        self.index_candidatura_atual = 0
        posicao_scroll = 0

        while True:
            max_linhas, _ = self.tela.getmaxyx()
            itens_exibidos = max_linhas - 5

            self.exibir_menu(opcoes_menu, posicao_scroll, itens_exibidos)

            result = self.interpreta_teclado(opcoes_menu)
            if result is not None:
                return result

    def escolha_candidatura(self):
        index_candidatura_escolhida = "nenhum"
        while index_candidatura_escolhida in FILTROS.keys():
            filtro = ""
            if index_candidatura_escolhida not in ["limpa_filtro", "nenhum"]:
                self.tela.clear()
                filtro = questionary.text(
                    f"Insira o {index_candidatura_escolhida} que deseja filtrar: ",
                    default="",
                ).ask()

            candidaturas = self.controller.candidaturas_filtradas(
                filtro, index_candidatura_escolhida
            )
            index_candidatura_escolhida = self.menu_candidaturas(candidaturas)

        return candidaturas[index_candidatura_escolhida]

    def exibe_mensagem_sucesso(self, novo_status, campo_atualizado="Status"):
        """
        Exibe uma mensagem de sucesso ao usuário quando o status é atualizado.
        """
        self.tela.clear()
        self.tela.addstr(
            5, 5, f"✅ {campo_atualizado} atualizado para: {novo_status}", curses.A_BOLD
        )
        self.tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        self.tela.getch()  # Espera pressionar uma tecla

    def exibe_mensagem_erro(self, erro):
        """
        Exibe uma mensagem de erro ao usuário em caso de falha.
        """
        self.tela.clear()
        self.tela.addstr(5, 5, f"❌ Ocorreu um erro: {str(erro)}", curses.A_BOLD)
        self.tela.addstr(7, 5, "Voltando ao menu principal...")
        raise RetornarMenuException
