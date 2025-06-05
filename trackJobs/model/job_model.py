from .repositories.SQLite.sqlite_empresa_repository import SQLiteEmpresaRepository
from .repositories.SQLite.sqlite_vaga_repository import SQLiteVagaRepository
from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.services.candidatura_service import CandidaturaService
from trackJobs.model.services.validadores.empresa_validador_service import (
    EmpresaValidadorService,
)
from trackJobs.model.services.validadores.vaga_validador_service import (
    VagaValidadorService,
)
from trackJobs.model.services.validadores.validador_service import ValidadorService


class JobModel:
    def __init__(self, db_path: str = "track_jobs.db"):
        self.db = BancoDeDados(db_path)
        empresa_repository = SQLiteEmpresaRepository(self.db)
        vaga_repository = SQLiteVagaRepository(self.db)
        self.candidatura_service = CandidaturaService(
            empresa_repository, vaga_repository
        )

    def cadastro(self, dados_candidatura: Vaga):
        """Cadastra uma nova candidatura"""
        try:
            self.candidatura_service.cadastra_candidatura(dados_candidatura)
        except TrackJobsException as e:
            raise e

    def validar_campo(self, campo, valor):
        """Valida o campo de acordo com os validadores definidos"""
        empresa_validador = EmpresaValidadorService(SQLiteEmpresaRepository(self.db))
        vaga_validador = VagaValidadorService(SQLiteVagaRepository(self.db))
        validador_service = ValidadorService(empresa_validador, vaga_validador)
        return validador_service.VALIDADORES[campo](valor)

    def campos_cadastro_vaga(self):
        """Retorna os campos necessários para cadastro de vaga"""
        vaga_repository = SQLiteVagaRepository(self.db)
        return vaga_repository.listar_campos_vaga()

    def campos_cadastro_empresa(self):
        """Retorna os campos necessários para cadastro de empresa"""
        empresa_repository = SQLiteEmpresaRepository(self.db)
        return empresa_repository.listar_campos_empresa()

    def listar_nome_empresas(self):
        """Retorna lista de empresas cadastradas"""
        empresa_repository = SQLiteEmpresaRepository(self.db)
        return empresa_repository.listar_nome_empresas()

    def get_empresa(self, nome_empresa):
        """Retorna os dados de uma empresa através do nome"""
        empresa_repository = SQLiteEmpresaRepository(self.db)
        return empresa_repository.buscar_empresa_por_nome(nome_empresa)

    def get_vaga_por_link(self, link: str):
        """Busca uma vaga pelo link"""
        return self.candidatura_service.get_vaga_por_link(link)

    def candidaturas_filtradas(self, filtro: str = "", tipo_filtro: str = ""):
        """Filtra candidaturas com base no nome ou descrição"""
        return self.candidatura_service.filtra_vagas(filtro, tipo_filtro)

    def atualizar_vaga(self, vaga: Vaga, campo_update: str, novo_dado: str):
        """Atualiza uma vaga existente"""
        return self.candidatura_service.atualiza_vaga(vaga, campo_update, novo_dado)
