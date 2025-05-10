import curses
import textwrap

from .exceptions import RetornarMenuException
from .menu import Menu
from .utils import get_vaga

VOLTAR_MENU = 27
MOVER_CIMA = curses.KEY_UP
MOVER_BAIXO = curses.KEY_DOWN


class MenuVisualizacao(Menu):
    def __init__(self, tela, db_path="track_jobs.db"):
        msg_menu = (
            "Selecione uma candidatura para visualizar os detalhes "
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)"
        )
        super().__init__(tela, msg_menu, db_path)
        self.max_linhas, self.max_colunas = self.tela.getmaxyx()
        self.conteudo = []

    def set_conteudo(self, candidatura):
        self.conteudo.clear()
        col_max = self.max_colunas - 4  # margem

        for chave, valor in candidatura.items():
            if chave == "data_aplicaçao":
                chave = "data de aplicação"
            elif chave == "descriçao":
                chave = "descrição"
            if valor is None:
                valor = ""
            if chave not in ["id", "idEmpresa"]:
                self.conteudo.append(f"{chave.capitalize()}:")
                self.conteudo.extend(textwrap.wrap(str(valor), width=col_max))
                self.conteudo.append("")  # espaço entre campos

    def exibir_campo(self, conteudo, scroll):
        self.tela.clear()
        for i in range(self.max_linhas - 2):
            if i + scroll >= len(conteudo):
                break

            linha = conteudo[i + scroll]

            if linha.endswith(":"):
                self.tela.addstr(i, 2, linha, curses.A_BOLD)
            else:
                self.tela.addstr(i, 2, linha)

        self.tela.addstr(
            self.max_linhas - 1,
            2,
            "⬆⬇ para rolar, aperte ESC para voltar.",
            curses.A_DIM,
        )

    def menu_da_candidatura(self, candidatura):
        self.tela.clear()
        scroll = 0
        self.set_conteudo(candidatura)

        while True:
            self.exibir_campo(self.conteudo, scroll)

            entrada_user = self.tela.getch()

            if entrada_user == MOVER_BAIXO and scroll + self.max_linhas - 2 < len(
                self.conteudo
            ):
                scroll += 1
            elif entrada_user == MOVER_CIMA and scroll > 0:
                scroll -= 1
            elif entrada_user == VOLTAR_MENU:
                break


def visualizacao_candidatura(tela, db_path="track_jobs.db"):
    menu = MenuVisualizacao(tela, db_path)
    try:
        while True:
            cand_selecionada = menu.escolha_candidatura()
            cand_selecionada = get_vaga(menu.db, cand_selecionada["link"])
            menu.menu_da_candidatura(cand_selecionada)

    except RetornarMenuException:
        pass

    except Exception as e:
        menu.exibe_mensagem_erro(e)
