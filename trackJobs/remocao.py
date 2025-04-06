import curses
import sqlite3

import questionary

from .exceptions import RetornarMenuException
from .menu import FILTROS
from .menu import Menu
from .utils import filtra_candidaturas


class MenuRemocao(Menu):
    def __init__(self, tela):
        super().__init__(tela)

    def exibe_mensagem_sucesso(self, novo_status, campo_atualizado="Status"):
        self.tela.clear()
        self.tela.addstr(5, 5, "✅ Candidatura removida com sucesso!", curses.A_BOLD)
        self.tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        self.tela.getch()


def realiza_remocao(db_path, candidatura):
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()
    comando = f"DELETE FROM vagas WHERE link = '{candidatura['link']}'"
    cursor.execute(comando)
    conexao.commit()
    conexao.close()


def remocao(tela, db_path="track_jobs.db"):
    try:
        menu_remocao = MenuRemocao(tela)
        index_candidatura = "nenhum"

        certainty = False
        while index_candidatura in FILTROS.keys() and not certainty:
            candidaturas = filtra_candidaturas(db_path, index_candidatura)
            index_candidatura = menu_remocao.menu_candidaturas(candidaturas)
            certainty = questionary.confirm(
                "Você tem certeza que deseja remover a candidatura "
                f"{candidaturas[index_candidatura]['nome']}?",
            ).ask()

        cand_selecionada = candidaturas[index_candidatura]
        realiza_remocao(db_path, cand_selecionada)

        menu_remocao.tela.clear()
        menu_remocao.exibe_mensagem_sucesso(None)

    except RetornarMenuException:
        pass

    except Exception as e:
        menu_remocao.exibe_mensagem_erro(e)
