import curses
import sqlite3

import questionary
from rich.console import Console

from .exceptions import RetornarMenuException

console = Console()
MOVER_BAIXO = curses.KEY_DOWN
MOVER_CIMA = curses.KEY_UP
CANDIDATURA_SELECIONADA = 10
VOLTAR_MENU = 27
OPCOES_STATUS = ["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"]
FILTRO_NOME = 0
FILTRO_LINK = 1
FILTRO_STATUS = 2
SEM_FILTRO = -1
MENU_VAZIO = 3


def get_candidaturas(filtro="", tipo_filtro=None):
    conexao = sqlite3.connect("track_jobs.db")
    conexao.row_factory = sqlite3.Row  # Configura para retornar dicionários
    cursor = conexao.cursor()
    if filtro:
        if tipo_filtro == FILTRO_LINK:
            cursor.execute(
                "SELECT nome, link, status FROM vagas WHERE link LIKE ?",
                (f"%{filtro}%",),
            )
        elif tipo_filtro == FILTRO_NOME:
            cursor.execute(
                "SELECT nome, link, status FROM vagas WHERE nome LIKE ?",
                (f"%{filtro}%",),
            )
        elif tipo_filtro == FILTRO_STATUS:
            cursor.execute(
                "SELECT nome, link, status FROM vagas WHERE status LIKE ?",
                (f"%{filtro}%",),
            )
    else:
        cursor.execute("SELECT nome, link, status FROM vagas")

    candidaturas = []
    for row in cursor.fetchall():
        candidaturas.append(dict(row))  # os dados de cada candidatura é um dict

    conexao.close()
    return candidaturas


def menu_candidaturas(tela, opcoes_menu: list):
    opcoes_menu.insert(0, "Filtrar por status")
    opcoes_menu.insert(0, "Filtrar por link")
    opcoes_menu.insert(0, "Filtrar por nome")

    curses.curs_set(0)  # Oculta o cursor no terminal para não aparecer piscando
    tela.keypad(True)
    tela.clear()

    index_candidatura_atual = 0
    posicao_scroll = 0

    while True:
        tela.clear()

        max_linhas, _ = tela.getmaxyx()
        itens_exibidos = max_linhas - 5
        msg = (
            "Selecione uma candidatura para editar "
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)"
        )
        tela.addstr(
            0,
            0,
            msg,
        )

        # Ajusta o scroll para manter o item selecionado visível
        if index_candidatura_atual < posicao_scroll:
            posicao_scroll = index_candidatura_atual
        elif index_candidatura_atual >= posicao_scroll + itens_exibidos:
            posicao_scroll = index_candidatura_atual - itens_exibidos + 1

        # Exibe apenas os itens visíveis na tela
        for i in range(itens_exibidos):
            cand_pra_print = i + posicao_scroll
            if cand_pra_print >= len(opcoes_menu):
                break  # Evita tentar acessar índices fora da lista

            c = opcoes_menu[cand_pra_print]  # Obtém a candidatura correspondente
            if type(c) is str:
                if cand_pra_print == index_candidatura_atual:
                    tela.addstr(
                        i + 2, 2, f"> {c}", curses.A_BOLD and curses.A_REVERSE
                    )  # Destaca item selecionado

                else:
                    tela.addstr(i + 2, 2, f"> {c}", curses.A_BOLD)  #

            else:
                if cand_pra_print == index_candidatura_atual:
                    tela.addstr(
                        i + 2, 2, f"> {c['nome']} - {c['status']}", curses.A_REVERSE
                    )  # Destaca item selecionado
                else:
                    tela.addstr(
                        i + 2, 2, f"  {c['nome']} - {c['status']}"
                    )  # Mostra item normal

        # Exibir tooltip no rodapé com o link completo da candidatura selecionada
        if type(opcoes_menu[index_candidatura_atual]) is not str:
            tela.addstr(
                max_linhas - 2, 2, "📎 Link da vaga selecionada: ", curses.A_BOLD
            )
            tela.addstr(
                max_linhas - 2,
                31,
                opcoes_menu[index_candidatura_atual]["link"],
                curses.A_UNDERLINE,
            )

        if len(opcoes_menu) == MENU_VAZIO:
            tela.addstr(i + 2, 2, "Nenhuma candidatura encontrada", curses.A_BOLD)
        entrada_user = tela.getch()  # Aguarda entrada do teclado

        # Movimentação da seleção para cima e para baixo
        if (
            entrada_user == MOVER_BAIXO
            and index_candidatura_atual < len(opcoes_menu) - 1
        ):
            index_candidatura_atual += 1
        elif entrada_user == MOVER_CIMA and index_candidatura_atual > 0:
            index_candidatura_atual -= 1
        elif entrada_user == CANDIDATURA_SELECIONADA:
            tela.clear()
            return index_candidatura_atual
        elif entrada_user == VOLTAR_MENU:
            tela.clear()
            raise RetornarMenuException


def menu_status(candidatura):
    novo_status = questionary.select(
        f"\n\n\nEditar status da candidatura {candidatura['nome']} para:",
        choices=OPCOES_STATUS,
    ).ask()

    return novo_status


def atualiza_cand(candidatura, novo_status):
    comando = (
        "UPDATE vagas "
        f"SET status='{novo_status}' "
        f"where link='{candidatura['link']}' "
        "LIMIT 1"
    )

    conexao = sqlite3.connect("track_jobs.db")
    cursor = conexao.cursor()
    cursor.execute(comando)
    conexao.commit()
    conexao.close()


def edita_status(tela):
    try:
        index_candidatura = SEM_FILTRO

        while index_candidatura in (
            FILTRO_LINK,
            FILTRO_NOME,
            FILTRO_STATUS,
            SEM_FILTRO,
        ):
            if index_candidatura == FILTRO_LINK:
                filtro_link = questionary.text(
                    "\nDigite o link da candidatura para filtrar:\n"
                ).ask()
                candidaturas = get_candidaturas(
                    filtro=filtro_link, tipo_filtro=FILTRO_LINK
                )
            elif index_candidatura == FILTRO_NOME:
                filtro_nome = questionary.text(
                    "\nDigite o nome da candidatura para filtrar:\n"
                ).ask()
                candidaturas = get_candidaturas(
                    filtro=filtro_nome, tipo_filtro=FILTRO_NOME
                )
            elif index_candidatura == FILTRO_STATUS:
                filtro_status = questionary.select(
                    "\nSelecione o status da candidatura para filtrar:\n",
                    choices=OPCOES_STATUS,
                ).ask()
                candidaturas = get_candidaturas(
                    filtro=filtro_status, tipo_filtro=FILTRO_STATUS
                )
            else:
                candidaturas = get_candidaturas()
            index_candidatura = menu_candidaturas(tela, candidaturas)
            pass

        cand_selecionada = candidaturas[index_candidatura]
        novo_status = menu_status(cand_selecionada)
        atualiza_cand(cand_selecionada, novo_status)

        tela.clear()
        tela.addstr(5, 5, f"✅ Status atualizado para: {novo_status}", curses.A_BOLD)
        tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        tela.getch()  # Espera pressionar uma tecla

    except RetornarMenuException:
        pass
