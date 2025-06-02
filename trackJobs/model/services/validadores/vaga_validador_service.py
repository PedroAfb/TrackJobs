from datetime import date

import validators

from trackJobs.exceptions import DataInvalidaException
from trackJobs.exceptions import NomeVazioException
from trackJobs.exceptions import StatusInvalidoException
from trackJobs.exceptions import URLInvalidaException
from trackJobs.exceptions import URLJaCadastradaException
from trackJobs.model.repositories.interfaces.vaga_repository import VagaRepository


class VagaValidadorService:
    def __init__(self, vaga_repository: VagaRepository):
        self.vaga_repository = vaga_repository

    def valida_nome(self, nome: str):
        if not nome:
            raise NomeVazioException()

        return True

    def valida_link(self, link: str):
        if not link:
            raise URLInvalidaException()

        elif validators.url(link):
            vaga = self.vaga_repository.buscar_vaga_por_link(link)

            if vaga is None:
                return True

            raise URLJaCadastradaException()

        else:
            raise URLInvalidaException()

    def valida_status(self, status: str):
        status = status.strip().lower()
        if status not in [
            "candidatar-se",
            "em análise",
            "entrevista",
            "rejeitado",
            "aceito",
        ]:
            raise StatusInvalidoException()

        return True

    def valida_data_aplicacao(self, data: str):
        if not data:
            return True
        try:
            date.fromisoformat(data)
            return True
        except ValueError:
            raise DataInvalidaException()
