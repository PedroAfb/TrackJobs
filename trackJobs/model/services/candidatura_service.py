from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.repositories.interfaces.empresa_repository import EmpresaRepository
from trackJobs.model.repositories.interfaces.vaga_repository import VagaRepository


class CandidaturaService:
    def __init__(
        self, empresa_repository: EmpresaRepository, vaga_repository: VagaRepository
    ):
        self.empresa_repository = empresa_repository
        self.vaga_repository = vaga_repository

    def cadastra_candidatura(self, vaga: Vaga):
        if vaga.empresa and not self.empresa_repository.buscar_empresa_por_nome(
            vaga.empresa.nome
        ):
            vaga.empresa.id = self.empresa_repository.cadastrar_empresa(vaga.empresa)
        self.vaga_repository.cadastrar_candidatura(vaga)
