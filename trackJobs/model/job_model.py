from .cadastro import cadastra_candidatura
from .cadastro import get_campos_cadastro_empresa
from .cadastro import get_campos_cadastro_vaga
from .cadastro import get_empresa_por_nome
from .validador import VALIDADORES
from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.exceptions import TrackJobsException


class JobModel:
    def __init__(self, db_path: str = "track_jobs.db"):
        self.db = BancoDeDados(db_path)

    def cadastro(self, dados_candidatura):
        """Cadastra uma nova candidatura"""
        cadastra_candidatura(dados_candidatura)

    def validar_campo(self, campo, valor, console):
        """Valida o campo de acordo com os validadores definidos"""
        if campo in VALIDADORES:
            try:
                return VALIDADORES[campo](self.db, valor, console)
            except TrackJobsException as e:
                raise e
        return False

    def campos_cadastro_vaga(self):
        """Retorna os campos necessários para cadastro de vaga"""
        return get_campos_cadastro_vaga(self.db)

    def campos_cadastro_empresa(self):
        """Retorna os campos necessários para cadastro de empresa"""
        return get_campos_cadastro_empresa(self.db)

    def listar_nome_empresas(self):
        """Retorna lista de empresas cadastradas"""
        cursor = self.db.cursor
        cursor.execute("SELECT nome FROM empresas ORDER BY nome")
        empresas = [row[0].capitalize() for row in cursor.fetchall()]
        return empresas

    def get_empresa(self, nome_empresa):
        """Retorna os dados de uma empresa através do nome"""
        return get_empresa_por_nome(self.db, nome_empresa)
