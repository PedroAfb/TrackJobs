import curses
import sqlite3

import questionary

from .exceptions import RetornarMenuException
from .menu import FILTROS
from .menu import Menu
from .utils import filtra_candidaturas


class MenuRemocao(Menu):
    def __init__(self, tela):
        msg_menu = (
            "Selecione uma candidatura para remover "
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)"
        )
        super().__init__(tela, msg_menu)

    def escolha_candidatura(self, db_path="track_jobs.db"):
        index_candidatura_escolhida = "nenhum"

        certainty = False
        while True:
            candidaturas = filtra_candidaturas(db_path, index_candidatura_escolhida)
            index_candidatura_escolhida = self.menu_candidaturas(candidaturas)

            if index_candidatura_escolhida not in FILTROS.keys():
                certainty = questionary.confirm(
                    "\n\nVocê tem certeza que deseja remover a candidatura "
                    f"{candidaturas[index_candidatura_escolhida]['nome']}?",
                ).ask()

                if certainty:
                    break

        return candidaturas[index_candidatura_escolhida]

    def exibe_mensagem_sucesso(self, novo_status, campo_atualizado="Status"):
        self.tela.clear()
        self.tela.addstr(5, 5, "✅ Candidatura removida com sucesso!", curses.A_BOLD)
        self.tela.addstr(7, 5, "Pressione qualquer tecla para voltar ao menu principal")
        self.tela.getch()


def realiza_remocao(db_path, candidatura):
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()
    comando = "DELETE FROM vagas WHERE link = ?"
    cursor.execute(comando, (candidatura["link"],))
    conexao.commit()
    conexao.close()


def remocao(tela, db_path="track_jobs.db"):
    menu_remocao = MenuRemocao(tela)
    try:
        cand_selecionada = menu_remocao.escolha_candidatura(db_path)
        realiza_remocao(db_path, cand_selecionada)

        menu_remocao.tela.clear()
        menu_remocao.exibe_mensagem_sucesso(None)

    except RetornarMenuException:
        pass

    except Exception as e:
        menu_remocao.exibe_mensagem_erro(e)
