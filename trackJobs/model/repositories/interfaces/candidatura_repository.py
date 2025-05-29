from typing import Protocol

from trackJobs.model.entities.candidatura import Candidatura


class CandidaturaRepository(Protocol):
    def cadastrar_candidatura(self, candidatura: Candidatura) -> None:
        """Cadastra uma nova candidatura"""
        ...
