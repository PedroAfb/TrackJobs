from typing import Optional
from typing import Protocol

from trackJobs.model.entities.empresa import Empresa


class EmpresaRepository(Protocol):
    def cadastrar_empresa(self, empresa: Empresa) -> None:
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
