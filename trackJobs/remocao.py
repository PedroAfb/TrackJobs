import curses

import questionary

from .exceptions import RetornarMenuException
from .menu import FILTROS
from .menu import Menu
from .utils import filtra_candidaturas
from trackJobs.banco_de_dados import BancoDeDados


class MenuRemocao(Menu):
    def __init__(self, tela, db_path="track_jobs.db"):
        msg_menu = (
            "Selecione uma candidatura para remover "
            "(Setas para navegar, Enter para selecionar "
            "e ESC para retornar ao menu principal)"
        )
        super().__init__(tela, msg_menu, db_path)

    def escolha_candidatura(self):
        index_candidatura_escolhida = "nenhum"

        certainty = False
        while True:
            candidaturas = filtra_candidaturas(self.db, index_candidatura_escolhida)
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


def realiza_remocao(db: BancoDeDados, candidatura):
    conexao = db.conexao
    cursor = db.cursor
    comando = "DELETE FROM vagas WHERE link = ?"
    cursor.execute(comando, (candidatura["link"],))
    conexao.commit()


def remocao(tela, db_path="track_jobs.db"):
    menu_remocao = MenuRemocao(tela, db_path)
    try:
        cand_selecionada = menu_remocao.escolha_candidatura()
        realiza_remocao(menu_remocao.db, cand_selecionada)

        menu_remocao.tela.clear()
        menu_remocao.exibe_mensagem_sucesso(None)

    except RetornarMenuException:
        pass

    except Exception as e:
        menu_remocao.exibe_mensagem_erro(e)
