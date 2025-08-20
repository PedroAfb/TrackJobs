from trackJobs.exceptions import CampoInvalidoException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.empresa import EmpresaQuery
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.entities.vaga import VagaQuery
from trackJobs.model.repositories.interfaces.empresa_repository import EmpresaRepository
from trackJobs.model.repositories.interfaces.vaga_repository import VagaRepository
from trackJobs.model.services.validadores.empresa_validador_service import (
    EmpresaValidadorService,
)
from trackJobs.model.services.validadores.vaga_validador_service import (
    VagaValidadorService,
)


class CandidaturaService:
    def __init__(
        self, empresa_repository: EmpresaRepository, vaga_repository: VagaRepository
    ):
        self.empresa_repository = empresa_repository
        self.vaga_repository = vaga_repository

    def cadastra_candidatura(self, vaga: Vaga):
        """Cadastra uma nova candidatura,
        em que seus dados já foram validados, no banco de dados"""
        empresa = None
        if vaga.empresa:
            empresa = self.empresa_repository.buscar_empresa_por_nome(vaga.empresa.nome)
            if not empresa:
                empresa = self.empresa_repository.cadastrar_empresa(vaga.empresa)

        vaga.empresa = empresa
        return self.vaga_repository.cadastrar_candidatura(vaga)

    def cadastra_empresa(self, empresa: Empresa):
        """Cadastra uma nova empresa no banco de dados"""
        empresa = self.empresa_repository.cadastrar_empresa(empresa)
        return empresa.id

    def filtra_vagas(self, filtro: str = "", tipo_filtro: str = "") -> list[Vaga]:
        """Filtra vagas com base no nome, link ou status"""
        return self.vaga_repository.get_vaga_com_filtro(filtro, tipo_filtro)

    def get_vagas(self, filtro: VagaQuery) -> list[Vaga]:
        """Filtra vagas com base no nome, link ou status"""
        return self.vaga_repository.get_vaga(filtro)

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

    def remove_vaga(self, vaga: Vaga):
        """Remove uma vaga existente"""
        self.vaga_repository.remover_vaga(vaga)

    def get_empresas(self, filtro: EmpresaQuery) -> list[Empresa]:
        """Busca empresas com base no filtro fornecido"""
        return self.empresa_repository.get_empresas(filtro)

    def valida_empresa(self, empresa: Empresa) -> bool:
        """Valida os dados de uma empresa antes do cadastro"""
        validador = EmpresaValidadorService(self.empresa_repository)
        if validador.valida_nome_empresa(
            empresa.nome
        ) and validador.valida_link_empresa(empresa.site):
            return True
        return False

    def valida_vaga(self, vaga: Vaga) -> bool:
        """Valida os dados de uma vaga antes do cadastro"""
        validador = VagaValidadorService(self.vaga_repository)
        if (
            validador.valida_nome(vaga.nome)
            and validador.valida_link(vaga.link)
            and validador.valida_status(vaga.status)
            and validador.valida_data_aplicacao(vaga.data_aplicacao)
        ):
            return True
        return False
