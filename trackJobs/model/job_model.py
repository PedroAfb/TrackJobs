from .repositories.SQLite.sqlite_empresa_repository import SQLiteEmpresaRepository
from .repositories.SQLite.sqlite_vaga_repository import SQLiteVagaRepository
from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.empresa import EmpresaQuery
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.entities.vaga import VagaQuery
from trackJobs.model.entities.vaga import VagaUpdate
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
        self.empresa_repository = SQLiteEmpresaRepository(self.db)
        self.vaga_repository = SQLiteVagaRepository(self.db)
        self.candidatura_service = CandidaturaService(
            self.empresa_repository, self.vaga_repository
        )

    def cadastro(self, dados_candidatura: Vaga):
        """Cadastra uma nova candidatura"""
        try:
            return self.candidatura_service.cadastra_candidatura(dados_candidatura)
        except TrackJobsException as e:
            raise e

    def cadastra_empresa(self, empresa: Empresa):
        """Cadastra uma nova empresa"""
        try:
            return self.candidatura_service.cadastra_empresa(empresa)
        except TrackJobsException as e:
            raise e

    def validar_campo(self, campo, valor):
        """Valida o campo de acordo com os validadores definidos"""
        empresa_validador = EmpresaValidadorService(self.empresa_repository)
        vaga_validador = VagaValidadorService(self.vaga_repository)
        validador_service = ValidadorService(empresa_validador, vaga_validador)
        return validador_service.VALIDADORES[campo](valor)

    def campos_cadastro_vaga(self):
        """Retorna os campos necessários para cadastro de vaga"""
        return self.vaga_repository.listar_campos_vaga()

    def campos_cadastro_empresa(self):
        """Retorna os campos necessários para cadastro de empresa"""
        return self.empresa_repository.listar_campos_empresa()

    def listar_nome_empresas(self):
        """Retorna lista de empresas cadastradas"""
        return self.empresa_repository.listar_nome_empresas()

    def get_empresa(self, nome_empresa):
        """Retorna os dados de uma empresa através do nome"""
        return self.empresa_repository.buscar_empresa_por_nome(nome_empresa)

    def get_vaga_por_link(self, link: str):
        """Busca uma vaga pelo link"""
        return self.candidatura_service.get_vaga_por_link(link)

    def candidaturas_filtradas(self, filtro: str = "", tipo_filtro: str = ""):
        """Filtra candidaturas com base no nome ou descrição"""
        return self.candidatura_service.filtra_vagas(filtro, tipo_filtro)

    def get_vagas(self, filtro: VagaQuery):
        """Filtra candidaturas com base no nome ou descrição"""
        return self.candidatura_service.get_vagas(filtro)

    def atualizar_vaga(self, vaga: Vaga, campo_update: str, novo_dado: str):
        """Atualiza uma vaga existente"""
        return self.candidatura_service.atualiza_vaga(vaga, campo_update, novo_dado)

    def atualiza_campos_vaga(self, vaga: VagaUpdate, dados_update: dict):
        """Atualiza múltiplos campos de uma vaga existente"""
        return self.candidatura_service.atualiza_campos_vaga(vaga, dados_update)

    def remover_vaga(self, vaga: Vaga):
        """Remove uma vaga existente"""
        return self.candidatura_service.remove_vaga(vaga)

    def get_empresas(self, filtro: EmpresaQuery) -> list[Empresa]:
        """Busca empresas com base no filtro fornecido"""
        return self.candidatura_service.get_empresas(filtro)

    def validar_empresa(self, empresa: Empresa) -> bool:
        """Valida os dados de uma empresa antes do cadastro"""
        return self.candidatura_service.valida_empresa(empresa)

    def validar_vaga(self, vaga: Vaga) -> bool:
        """Valida os dados de uma vaga antes do cadastro"""
        return self.candidatura_service.valida_vaga(vaga)
