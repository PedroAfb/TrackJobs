from .cadastro import cadastra_candidatura
from .cadastro import get_campos_cadastro_empresa
from .cadastro import get_campos_cadastro_vaga
from .cadastro import verifica_empresa_por_nome
from .validador import VALIDADORES
from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.exceptions import TrackJobsException


class JobModel:
    def __init__(self, db_path: str = "track_jobs.db"):
        self.db = BancoDeDados(db_path)

    def cadastro(self, dados_candidatura):
        cadastra_candidatura(dados_candidatura)

    def validar_campo(self, campo, valor, console):
        if campo in VALIDADORES:
            try:
                return VALIDADORES[campo](self.db, valor, console)
            except TrackJobsException as e:
                raise e
        return False

    def campos_cadastro_vaga(self):
        return get_campos_cadastro_vaga(self.db)

    def campos_cadastro_empresa(self):
        return get_campos_cadastro_empresa(self.db)

    def listar_nome_empresas(self):
        """Retorna lista de empresas cadastradas"""
        cursor = self.db.cursor
        cursor.execute("SELECT nome FROM empresas ORDER BY nome")
        empresas = [row[0].capitalize() for row in cursor.fetchall()]
        return empresas

    def get_id_empresa(self, nome_empresa):
        """Retorna o ID da empresa pelo nome"""
        self.db.cursor.execute(
            "SELECT id FROM empresas WHERE nome = ? LIMIT 1", (nome_empresa,)
        )
        dados = self.db.cursor.fetchone()

        if dados:
            return {"id_empresa": dados[0]}
        return None

    def get_nome_empresa(self, id_empresa):
        """Retorna o nome da empresa pelo ID"""
        self.db.cursor.execute(
            "SELECT nome FROM empresas WHERE id = ? LIMIT 1", (id_empresa,)
        )
        dados = self.db.cursor.fetchone()

        if dados:
            return {"nome_empresa": dados[0]}
        return None

    def empresa_existe(self, nome_empresa):
        """Verifica se empresa já existe"""
        return verifica_empresa_por_nome(self.db, nome_empresa) is not None
