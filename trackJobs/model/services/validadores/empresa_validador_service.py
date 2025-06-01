import validators

from trackJobs.exceptions import CampoDuplicadoException
from trackJobs.exceptions import NomeVazioException
from trackJobs.exceptions import URLInvalidaException
from trackJobs.exceptions import URLJaCadastradaException
from trackJobs.model.repositories.interfaces.empresa_repository import EmpresaRepository


class EmpresaValidadorService:
    def __init__(self, empresa_repository: EmpresaRepository):
        self.empresa_repository = empresa_repository

    def valida_nome_empresa(self, nome_empresa: str):
        if not nome_empresa:
            raise NomeVazioException()

        empresa_existe = self.empresa_repository.buscar_empresa_por_nome(nome_empresa)
        if empresa_existe:
            raise CampoDuplicadoException("Empresa já cadastrada.")

        return True

    def valida_link_empresa(self, link: str):
        if not link:
            return True

        elif validators.url(link):
            empresa = self.empresa_repository.buscar_empresa_por_link(link)
            if not empresa:
                return True

            raise URLJaCadastradaException()

        raise URLInvalidaException()
