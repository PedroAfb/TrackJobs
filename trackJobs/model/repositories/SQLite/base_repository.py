import sqlite3
from contextlib import contextmanager

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.exceptions import CampoDuplicadoException
from trackJobs.exceptions import ErroCandidaturaException


class BaseSQLiteRepository:
    """Classe base para todos os repositories SQLite"""

    def __init__(self, db: BancoDeDados):
        self.db = db

    @contextmanager
    def transaction(self):
        """Gerenciador de contexto para transações SQL"""
        try:
            yield self.db.cursor
            self.db.conexao.commit()
        except sqlite3.IntegrityError as e:
            self.db.conexao.rollback()
            erro_duplicado = str(e)
            campo_duplicado = erro_duplicado.split(" ")[-1]
            raise CampoDuplicadoException(
                f"Erro: O campo '{campo_duplicado}' já está cadastrado."
            )
        except sqlite3.DatabaseError as e:
            self.db.conexao.rollback()
            raise ErroCandidaturaException(f"Erro no banco de dados: {e}")
        except Exception as e:
            self.db.conexao.rollback()
            raise e
