import curses
import sqlite3

from .exceptions import RetornarMenuException
from .status import ajustar_scroll
from .status import CANDIDATURA_SELECIONADA
from .status import exibe_mensagem_erro
from .status import exibe_mensagem_sucesso
from .status import filtra_candidaturas
from .status import FILTROS
from .status import menu_candidaturas
from .status import MOVER_BAIXO
from .status import MOVER_CIMA
from .status import VOLTAR_MENU

CAMPOS_VAGA = ["nome", "link", "data_aplicacao", "status", "descricao"]


def get_vaga(db_path, link):
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()

    comando = f"SELECT * FROM vagas WHERE link = '{link}'"
    cursor.execute(comando)
    vaga = cursor.fetchone()

    conexao.close()
    if vaga:
        # Pega o nome das colunas
        colunas = [descricao[0] for descricao in cursor.description]

        # Cria um dicionário combinando as colunas com os valores
        vaga_dict = dict(zip(colunas, vaga))

        return vaga_dict
    else:
        return None  # Caso não encontre a vaga


def exibir_item(tela, campo, dados, i, campo_pra_print, index_campo_atual):
    if campo_pra_print == index_campo_atual:
        msg = f"> {campo.capitalize()}: {dados}\n"
    else:
        msg = f"> {campo.capitalize()}\n"

    estilo = (
        curses.A_REVERSE if campo_pra_print == index_campo_atual else curses.A_NORMAL
    )
    tela.addstr(i + 2, 2, msg, estilo)


def menu_edicao(tela, candidatura: dict):
    curses.curs_set(0)  # Oculta o cursor no terminal
    tela.keypad(True)
    tela.clear()

    index_campo_atual = 0
    posicao_scroll = 0

    while True:
        max_linhas, _ = tela.getmaxyx()
        itens_exibidos = max_linhas - 5

        tela.clear()
        max_linhas, _ = tela.getmaxyx()

        msg = (
            "Escolha o campo que queira editar da vaga escolhida abaixo:\n"
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)\n\n"
        )
        tela.addstr(0, 0, msg)

        posicao_scroll = ajustar_scroll(
            index_campo_atual, posicao_scroll, itens_exibidos
        )
        cont = 0
        for campo in CAMPOS_VAGA:
            campo_pra_print = cont + posicao_scroll
            exibir_item(
                tela,
                campo,
                candidatura[campo],
                cont + 1,
                campo_pra_print,
                index_campo_atual,
            )
            cont += 1

        entrada_user = tela.getch()  # Aguarda entrada do teclado

        # Movimentação da seleção para cima e para baixo
        if entrada_user == MOVER_BAIXO and index_campo_atual < len(CAMPOS_VAGA) - 1:
            index_campo_atual += 1
        elif entrada_user == MOVER_CIMA and index_campo_atual > 0:
            index_campo_atual -= 1
        elif entrada_user == CANDIDATURA_SELECIONADA:
            tela.clear()
            return CAMPOS_VAGA[index_campo_atual]
        elif entrada_user == VOLTAR_MENU:
            tela.clear()
            raise RetornarMenuException


def edicao(tela, db_path="track_jobs.db"):
    try:
        index_candidatura = FILTROS["nenhum"]

        while index_candidatura in FILTROS.values():
            candidaturas = filtra_candidaturas(db_path, index_candidatura)
            index_candidatura = menu_candidaturas(tela, candidaturas)

        # Seleciona a candidatura e atualiza o status
        cand_selecionada = candidaturas[index_candidatura]
        cand_selecionada = get_vaga(db_path, cand_selecionada["link"])
        # campo_selecionado = menu_edicao(tela, cand_selecionada)
        # Informe o novo valor do campo descricao:
        # Faz update no bando de dados

        exibe_mensagem_sucesso(tela, "Edição realizada com sucesso!")

    except RetornarMenuException:
        pass

    except Exception as e:
        exibe_mensagem_erro(tela, e)
