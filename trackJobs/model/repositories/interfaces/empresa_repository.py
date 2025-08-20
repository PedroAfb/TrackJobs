from typing import Optional
from typing import Protocol

from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.empresa import EmpresaQuery


class EmpresaRepository(Protocol):
    def cadastrar_empresa(self, empresa: Empresa) -> Empresa:
        ...

    def listar_nome_empresas(self) -> list[str]:
        ...

    def listar_campos_empresa(self) -> list[str]:
        """Retorna os campos necessários para cadastro de empresa"""
        ...

    def buscar_empresa_por_nome(self, nome: str) -> Optional[Empresa]:
        ...

    def buscar_empresa_por_link(self, link: str) -> Optional[Empresa]:
        """Retorna os dados de uma empresa através do link"""
        ...

    def get_empresas(self, filtro: EmpresaQuery) -> list[Empresa]:
        ...
