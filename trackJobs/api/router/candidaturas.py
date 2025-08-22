from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from trackJobs.api.dependencies import get_job_controller
from trackJobs.controller.api_job_controller import APIJobController
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.empresa import EmpresaPost
from trackJobs.model.entities.empresa import EmpresaQuery
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.entities.vaga import VagaPost
from trackJobs.model.entities.vaga import VagaQuery
from trackJobs.model.entities.vaga import VagaUpdate

router = APIRouter(tags=["empresas"])


@router.get("/empresas", response_model=list[Empresa])
def get_empresas(
    filtro_empresa: Annotated[EmpresaQuery, Query()],
    controller: APIJobController = Depends(get_job_controller),
) -> list[Empresa]:
    return controller.get_empresas(filtro_empresa)


@router.get("/vagas", response_model=list[Vaga])
def get_vagas(
    filtro_vaga: Annotated[VagaQuery, Query()],
    controller: APIJobController = Depends(get_job_controller),
) -> list[Vaga]:
    return controller.get_vagas(filtro_vaga)


@router.post("/vagas", response_model=dict)
def cadastra_vaga(
    vaga: VagaPost,
    controller: APIJobController = Depends(get_job_controller),
) -> dict:
    try:
        vaga_cadastrada = controller.cadastra_vaga(vaga)
        return {"message": "Vaga cadastrada com sucesso", "vaga": vaga_cadastrada}
    except TrackJobsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/empresas", response_model=dict)
def cadastra_empresa(
    empresa: EmpresaPost,
    controller: APIJobController = Depends(get_job_controller),
) -> dict:
    try:
        empresa_cadastrada = controller.cadastra_empresa(empresa)
        return {
            "message": "Empresa cadastrada com sucesso",
            "empresa": empresa_cadastrada,
        }
    except TrackJobsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/vagas/{vaga_id}", response_model=dict)
def atualiza_vaga(
    vaga_id: int,
    vaga: VagaUpdate,
    controller: APIJobController = Depends(get_job_controller),
) -> dict:
    try:
        vaga.id = vaga_id
        vaga_atualizada = controller.atualiza_vaga(vaga)
        return {"message": "Vaga atualizada com sucesso", "vaga": vaga_atualizada}
    except TrackJobsException as e:
        raise HTTPException(status_code=400, detail=str(e))
