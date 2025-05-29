from typing import Protocol


class VagaRepository(Protocol):
    def listar_campos_vaga(self) -> list[str]:
        """Retorna os campos necessários para cadastro de vaga"""
        ...
