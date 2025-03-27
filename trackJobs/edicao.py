import curses

import questionary

from .exceptions import RetornarMenuException
from .menu import CANDIDATURA_SELECIONADA
from .menu import FILTROS
from .menu import Menu
from .menu import MOVER_BAIXO
from .menu import MOVER_CIMA
from .menu import VOLTAR_MENU
from .utils import filtra_candidaturas
from .utils import get_vaga
from .utils import realiza_update

CAMPOS_VAGA = ["nome", "link", "data de aplicaçao", "status", "descriçao"]


class MenuEdicao(Menu):
    def __init__(self, tela):
        super().__init__(tela)
        self.index_campo_atual = 0

    def exibir_campo(self, campo, dados, i, campo_pra_print):
        _, largura = self.tela.getmaxyx()
        margem = 2  # Margem de segurança para evitar estouro

        if campo_pra_print == self.index_campo_atual:
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

    def interpreta_teclado(self, opcoes_menu):
        entrada_user = self.tela.getch()  # Aguarda entrada do teclado

        # Movimentação da seleção para cima e para baixo
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

            msg = (
                "Escolha o campo que queira editar da vaga escolhida abaixo:\n"
                "(Setas para navegar, Enter para selecionar "
                "e ESC para retornar ao menu principal)\n\n"
            )
            self.tela.addstr(0, 0, msg)

            self.index_candidatura_atual = self.index_campo_atual
            posicao_scroll = self.ajustar_scroll(posicao_scroll, itens_exibidos)
            # cont = 0
            for i, campo in enumerate(CAMPOS_VAGA):
                campo_pra_print = i + posicao_scroll
                self.exibir_campo(campo, candidatura[campo], i, campo_pra_print)
                # cont += 1

            result = self.interpreta_teclado(None)
            if result:
                return result

    def exibe_mensagem_sucesso(self, novo_status, campo_atualizado="Status"):
        self.tela.clear()
        self.tela.addstr(
            5, 5, f"✅ Campo {campo_atualizado} atualizado com sucesso!", curses.A_BOLD
        )
        self.tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        self.tela.getch()  # Espera pressionar uma tecla


def edicao(tela, db_path="track_jobs.db"):
    try:
        index_candidatura = "nenhum"
        menu_edicao = MenuEdicao(tela)
        menu = Menu(tela)

        while index_candidatura in FILTROS.keys():
            candidaturas = filtra_candidaturas(db_path, index_candidatura)
            index_candidatura = menu.menu_candidaturas(candidaturas)

        # Seleciona a candidatura e atualiza o status
        cand_selecionada = candidaturas[index_candidatura]
        cand_selecionada = get_vaga(db_path, cand_selecionada["link"])
        campo_selecionado = menu_edicao.menu_edicao(cand_selecionada)
        tela.clear()
        novo_dado = (
            questionary.text(
                "\nInforme o novo valor do campo "
                f"{campo_selecionado.capitalize()}:\n"
            )
            .ask()
            .strip()
        )
        # Faz update no bando de dados

        realiza_update(db_path, cand_selecionada, campo_selecionado, novo_dado)

        menu_edicao.exibe_mensagem_sucesso(tela, campo_selecionado.capitalize())

    except RetornarMenuException:
        pass

    except Exception as e:
        menu_edicao.exibe_mensagem_erro(e)
