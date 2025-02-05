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


def get_candidaturas():
    conexao = sqlite3.connect("track_jobs.db")
    conexao.row_factory = sqlite3.Row  # Configura para retornar dicionários
    cursor = conexao.cursor()

    cursor.execute("SELECT nome, link, status FROM vagas")
    candidaturas = []
    for row in cursor.fetchall():
        candidaturas.append(dict(row))  # os dados de cada candidatura é um dict

    conexao.close()
    return candidaturas


def menu_candidaturas(tela, candidaturas: list):
    curses.curs_set(0)  # Oculta o cursor no terminal para não aparecer piscando
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
            if cand_pra_print >= len(candidaturas):
                break  # Evita tentar acessar índices fora da lista

            c = candidaturas[cand_pra_print]  # Obtém a candidatura correspondente
            if cand_pra_print == index_candidatura_atual:
                tela.addstr(
                    i + 2, 2, f"> {c['nome']} - {c['status']}", curses.A_REVERSE
                )  # Destaca item selecionado
            else:
                tela.addstr(
                    i + 2, 2, f"  {c['nome']} - {c['status']}"
                )  # Mostra item normal

        # Exibir tooltip no rodapé com o link completo da candidatura selecionada
        tela.addstr(max_linhas - 2, 2, "📎 Link da vaga selecionada: ", curses.A_BOLD)
        tela.addstr(
            max_linhas - 2,
            31,
            candidaturas[index_candidatura_atual]["link"],
            curses.A_UNDERLINE,
        )

        entrada_user = tela.getch()  # Aguarda entrada do teclado

        # Movimentação da seleção para cima e para baixo
        if (
            entrada_user == MOVER_BAIXO
            and index_candidatura_atual < len(candidaturas) - 1
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
        candidaturas = get_candidaturas()

        index_candidatura = menu_candidaturas(tela, candidaturas)

        cand_selecionada = candidaturas[index_candidatura]
        novo_status = menu_status(cand_selecionada)
        atualiza_cand(cand_selecionada, novo_status)

        tela.clear()
        tela.addstr(5, 5, f"✅ Status atualizado para: {novo_status}", curses.A_BOLD)
        tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        tela.getch()  # Espera pressionar uma tecla

    except RetornarMenuException:
        pass
