import curses
import textwrap

from trackJobs.controller.job_controller import JobController
from trackJobs.view.menus.menu import Menu

VOLTAR_MENU = 27
MOVER_CIMA = curses.KEY_UP
MOVER_BAIXO = curses.KEY_DOWN
CAMPO_PARA_ITEM = {
    "data_aplicacao": "Data de Aplicação",
    "descricao": "Descrição",
    "nome_empresa": "Nome da Empresa",
    "site_empresa": "Site da Empresa",
    "setor_empresa": "Setor da Empresa",
}
CAMPO_NAO_VISIVEL = ["id", "id_empresa"]


class MenuVisualizacao(Menu):
    def __init__(self, tela, controller: JobController):
        msg_menu = (
            "Selecione uma candidatura para visualizar os detalhes "
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)"
        )
        super().__init__(tela, controller, msg_menu)
        self.max_linhas, self.max_colunas = self.tela.getmaxyx()
        self.conteudo = []

    def set_conteudo(self, candidatura):
        self.conteudo.clear()
        col_max = self.max_colunas - 4  # margem

        for chave, valor in candidatura.items():
            chave = CAMPO_PARA_ITEM.get(chave, chave)

            if valor is None:
                valor = ""
            if chave not in CAMPO_NAO_VISIVEL:
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
