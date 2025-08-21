from fastapi import HTTPException

from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.empresa import EmpresaPost
from trackJobs.model.entities.empresa import EmpresaQuery
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.entities.vaga import VagaPost
from trackJobs.model.entities.vaga import VagaQuery
from trackJobs.model.entities.vaga import VagaUpdate
from trackJobs.model.job_model import JobModel


class APIJobController:
    def __init__(self, job_model: JobModel):
        self.job_model = job_model

    def get_empresas(self, filtro: EmpresaQuery) -> list[Empresa]:
        return self.job_model.get_empresas(filtro)

    def get_vagas(self, filtro: VagaQuery) -> list[Vaga]:
        return self.job_model.get_vagas(filtro)

    def cadastra_vaga(self, vaga: VagaPost) -> int:
        try:
            if vaga.empresa:
                self.job_model.validar_empresa(vaga.empresa)

            self.job_model.validar_vaga(vaga)
            return self.job_model.cadastro(vaga)

        except TrackJobsException as e:
            raise e

    def cadastra_empresa(self, empresa: EmpresaPost) -> int:
        try:
            self.job_model.validar_empresa(empresa)
            return self.job_model.cadastra_empresa(empresa)
        except TrackJobsException as e:
            raise e

    def atualiza_vaga(self, vaga: VagaUpdate) -> Vaga:
        try:
            dados_update = {
                campo: valor
                for campo, valor in vaga.model_dump().items()
                if valor is not None and campo != "id"
            }

            if not dados_update:
                raise HTTPException(
                    status_code=400,
                    detail="Pelo menos um campo deve ser fornecido para atualização",
                )

            return self.job_model.atualiza_campos_vaga(vaga, dados_update)

        except TrackJobsException as e:
            raise e
