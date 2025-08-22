from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query

from trackJobs.api.dependencies import get_job_controller
from trackJobs.controller.api_job_controller import APIJobController
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.api_response import APIResponse
from trackJobs.model.entities.empresa import EmpresaPost
from trackJobs.model.entities.empresa import EmpresaQuery
from trackJobs.model.entities.vaga import VagaPost
from trackJobs.model.entities.vaga import VagaQuery
from trackJobs.model.entities.vaga import VagaUpdate

router = APIRouter(tags=["empresas"])


@router.get("/empresas", response_model=APIResponse)
def get_empresas(
    filtro_empresa: Annotated[EmpresaQuery, Query()],
    controller: APIJobController = Depends(get_job_controller),
) -> APIResponse:
    empresas = controller.get_empresas(filtro_empresa)
    return APIResponse(success=True, message="Empresas encontradas", data=empresas)


@router.get("/vagas", response_model=APIResponse)
def get_vagas(
    filtro_vaga: Annotated[VagaQuery, Query()],
    controller: APIJobController = Depends(get_job_controller),
) -> APIResponse:
    vagas = controller.get_vagas(filtro_vaga)
    return APIResponse(success=True, message="Vagas encontradas", data=vagas)


@router.post("/vagas", response_model=APIResponse)
def cadastra_vaga(
    vaga: VagaPost,
    controller: APIJobController = Depends(get_job_controller),
) -> APIResponse:
    try:
        vaga_cadastrada = controller.cadastra_vaga(vaga)
        return APIResponse(
            success=True, message="Vaga cadastrada com sucesso", data=vaga_cadastrada
        )
    except TrackJobsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/empresas", response_model=APIResponse)
def cadastra_empresa(
    empresa: EmpresaPost,
    controller: APIJobController = Depends(get_job_controller),
) -> APIResponse:
    try:
        empresa_cadastrada = controller.cadastra_empresa(empresa)
        return APIResponse(
            success=True,
            message="Empresa cadastrada com sucesso",
            data=empresa_cadastrada,
        )
    except TrackJobsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/vagas/{vaga_id}", response_model=APIResponse)
def atualiza_vaga(
    vaga_id: Annotated[int, Path(title="ID da vaga a ser atualizada")],
    vaga: VagaUpdate,
    controller: APIJobController = Depends(get_job_controller),
) -> APIResponse:
    try:
        vaga.id = vaga_id
        vaga_atualizada = controller.atualiza_vaga(vaga)
        return APIResponse(
            success=True, message="Vaga atualizada com sucesso", data=vaga_atualizada
        )
    except TrackJobsException as e:
        raise HTTPException(status_code=400, detail=str(e))
