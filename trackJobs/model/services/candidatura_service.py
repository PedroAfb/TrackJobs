from trackJobs.exceptions import CampoInvalidoException
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
        empresa = None
        if vaga.empresa:
            empresa = self.empresa_repository.buscar_empresa_por_nome(vaga.empresa.nome)
            if not empresa:
                empresa = self.empresa_repository.cadastrar_empresa(vaga.empresa)

        vaga.empresa = empresa
        self.vaga_repository.cadastrar_candidatura(vaga)

    def filtra_vagas(self, filtro: str = "", tipo_filtro: str = "") -> list[Vaga]:
        """Filtra vagas com base no nome ou descrição"""
        return self.vaga_repository.get_vaga_com_filtro(filtro, tipo_filtro)

    def get_vaga_por_link(self, link: str) -> Vaga:
        """Busca uma vaga pelo link"""
        return self.vaga_repository.buscar_vaga_por_link(link)

    def atualiza_vaga(self, vaga: Vaga, campo_update: str, novo_dado: str):
        """Atualiza uma vaga existente"""
        if campo_update not in self.vaga_repository.listar_campos_vaga():
            raise CampoInvalidoException(
                f"Campo '{campo_update}' não é válido para atualização."
            )
        self.vaga_repository.atualizar_vaga(vaga, campo_update, novo_dado)
