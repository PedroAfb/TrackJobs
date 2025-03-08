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
FILTROS = {"limpa_filtro": 0, "nome": 1, "link": 2, "status": 3, "nenhum": -1}
MENU_VAZIO = 4


def get_candidaturas(db_path, filtro="", tipo_filtro=None):
    conexao = sqlite3.connect(db_path)
    conexao.row_factory = sqlite3.Row  # Retorna os resultados como dicionário
    cursor = conexao.cursor()
    query = "SELECT nome, link, status FROM vagas"
    params = []

    if tipo_filtro in FILTROS.values():
        if tipo_filtro == FILTROS["link"]:
            coluna = "link"
        elif tipo_filtro == FILTROS["nome"]:
            coluna = "nome"
        elif tipo_filtro == FILTROS["status"]:
            coluna = "status"
        query += f" WHERE {coluna} LIKE ?"
        params.append(f"%{filtro}%")

    cursor.execute(query, params)
    candidaturas = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    return candidaturas


def exibir_menu(
    tela, opcoes_menu, index_candidatura_atual, posicao_scroll, itens_exibidos
):
    """
    Exibe o menu com as candidaturas e opções de filtro.
    """
    tela.clear()
    max_linhas, _ = tela.getmaxyx()

    msg = (
        "Selecione uma candidatura para editar "
        "(Setas para navegar, Enter para selecionar "
        "e ESC para retornar ao menu principal)"
    )
    tela.addstr(0, 0, msg)

    posicao_scroll = ajustar_scroll(
        index_candidatura_atual, posicao_scroll, itens_exibidos
    )

    for i in range(itens_exibidos):
        cand_pra_print = i + posicao_scroll
        if cand_pra_print >= len(opcoes_menu):
            break

        c = opcoes_menu[cand_pra_print]
        exibir_item(tela, c, i, cand_pra_print, index_candidatura_atual)

    # Exibe o link da candidatura selecionada no rodapé, se aplicável
    if type(opcoes_menu[index_candidatura_atual]) is not str:
        exibir_link(tela, max_linhas, opcoes_menu[index_candidatura_atual])

    if len(opcoes_menu) == MENU_VAZIO:
        tela.addstr(i + 2, 2, "Nenhuma candidatura encontrada", curses.A_BOLD)


def ajustar_scroll(index_candidatura_atual, posicao_scroll, itens_exibidos):
    """
    Ajusta a posição do scroll para manter o item selecionado visível.
    """
    if index_candidatura_atual < posicao_scroll:
        return index_candidatura_atual
    elif index_candidatura_atual >= posicao_scroll + itens_exibidos:
        return index_candidatura_atual - itens_exibidos + 1
    return posicao_scroll


def exibir_item(tela, c, i, cand_pra_print, index_candidatura_atual):
    """
    Exibe um item na tela, destacando o item selecionado.
    """
    if type(c) is str:
        estilo = (
            curses.A_BOLD | curses.A_REVERSE
            if cand_pra_print == index_candidatura_atual
            else curses.A_BOLD
        )
        tela.addstr(i + 2, 2, f"> {c}", estilo)
    else:
        estilo = (
            curses.A_REVERSE
            if cand_pra_print == index_candidatura_atual
            else curses.A_NORMAL
        )
        tela.addstr(i + 2, 2, f"  {c['nome']} - {c['status']}", estilo)


def exibir_link(tela, max_linhas, candidatura):
    """
    Exibe o link da candidatura selecionada.
    """
    tela.addstr(max_linhas - 2, 2, "📎 Link da vaga selecionada: ", curses.A_BOLD)
    tela.addstr(
        max_linhas - 2,
        31,
        candidatura["link"],
        curses.A_UNDERLINE,
    )


def menu_candidaturas(tela, opcoes_menu: list):
    """
    Exibe o menu principal de candidaturas e permite ao usuário navegar e selecionar.
    """
    opcoes_menu = [
        "Limpar filtro",
        "Filtrar por nome",
        "Filtrar por link",
        "Filtrar por status",
    ] + opcoes_menu

    curses.curs_set(0)  # Oculta o cursor no terminal
    tela.keypad(True)
    tela.clear()

    index_candidatura_atual = 0
    posicao_scroll = 0

    while True:
        max_linhas, _ = tela.getmaxyx()
        itens_exibidos = max_linhas - 5

        exibir_menu(
            tela, opcoes_menu, index_candidatura_atual, posicao_scroll, itens_exibidos
        )

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
            if index_candidatura_atual < MENU_VAZIO:
                return next(
                    (
                        chave
                        for chave, valor in FILTROS.items()
                        if valor == index_candidatura_atual
                    ),
                    None,
                )
            else:
                return index_candidatura_atual - MENU_VAZIO
        elif entrada_user == VOLTAR_MENU:
            tela.clear()
            raise RetornarMenuException


def menu_status(candidatura):
    novo_status = questionary.select(
        f"\n\n\nEditar status da candidatura {candidatura['nome']} para:",
        choices=OPCOES_STATUS,
    ).ask()

    return novo_status


def atualiza_cand(db_path, candidatura, novo_status):
    comando = (
        "UPDATE vagas "
        f"SET status='{novo_status}' "
        f"where link='{candidatura['link']}' "
        "LIMIT 1"
    )

    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()
    cursor.execute(comando)
    conexao.commit()
    conexao.close()


def filtra_candidaturas(db_path, index_candidatura):
    """
    Filtra as candidaturas com base na opção selecionada.
    """
    if index_candidatura == "link":
        filtro_link = questionary.text(
            "\nDigite o link da candidatura para filtrar:\n"
        ).ask()
        return get_candidaturas(
            db_path, filtro=filtro_link, tipo_filtro=FILTROS["link"]
        )

    elif index_candidatura == "nome":
        filtro_nome = questionary.text(
            "\nDigite o nome da candidatura para filtrar:\n"
        ).ask()
        return get_candidaturas(
            db_path, filtro=filtro_nome, tipo_filtro=FILTROS["nome"]
        )

    elif index_candidatura == "status":
        filtro_status = questionary.select(
            "\nSelecione o status da candidatura para filtrar:\n",
            choices=OPCOES_STATUS,
        ).ask()
        return get_candidaturas(
            db_path, filtro=filtro_status, tipo_filtro=FILTROS["status"]
        )

    return get_candidaturas(db_path)


def exibe_mensagem_sucesso_status(tela, novo_status, campo_atualizado="Status"):
    """
    Exibe uma mensagem de sucesso ao usuário quando o status é atualizado.
    """
    tela.clear()
    tela.addstr(
        5, 5, f"✅ {campo_atualizado} atualizado para: {novo_status}", curses.A_BOLD
    )
    tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
    tela.getch()  # Espera pressionar uma tecla


def exibe_mensagem_erro(tela, erro):
    """
    Exibe uma mensagem de erro ao usuário em caso de falha.
    """
    tela.clear()
    tela.addstr(5, 5, f"❌ Ocorreu um erro: {str(erro)}", curses.A_BOLD)
    tela.addstr(7, 5, "Voltando ao menu principal...")
    raise RetornarMenuException


def edita_status(tela, db_path="track_jobs.db"):
    try:
        index_candidatura = "nenhum"

        while index_candidatura in FILTROS.keys():
            candidaturas = filtra_candidaturas(db_path, index_candidatura)
            index_candidatura = menu_candidaturas(tela, candidaturas)

        # Seleciona a candidatura e atualiza o status
        cand_selecionada = candidaturas[index_candidatura]
        novo_status = menu_status(cand_selecionada)
        atualiza_cand(db_path, cand_selecionada, novo_status)

        exibe_mensagem_sucesso_status(tela, novo_status)

    except RetornarMenuException:
        pass

    except Exception as e:
        exibe_mensagem_erro(tela, e)
