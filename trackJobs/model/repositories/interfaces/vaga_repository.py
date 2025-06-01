from typing import Protocol

from trackJobs.model.entities.vaga import Vaga


class VagaRepository(Protocol):
    def listar_campos_vaga(self) -> list[str]:
        """Retorna os campos necessários para cadastro de vaga"""
        ...

    def cadastrar_candidatura(self, candidatura: Vaga) -> None:
        """Cadastra uma nova candidatura no banco de dados"""
        ...

    def buscar_vaga_por_link(self, link: str) -> Vaga:
        """Busca uma vaga pelo link"""
        ...
