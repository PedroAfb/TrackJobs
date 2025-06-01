from dataclasses import dataclass
from enum import Enum
from typing import Optional

from trackJobs.model.entities.empresa import Empresa


class VagaStatus(Enum):
    CANDIDATARSE = "Candidatar-se"
    EM_ANALISE = "Em análise"
    ENTREVISTA = "Entrevista"
    REJEITADO = "Rejeitado"
    ACEITO = "Aceito"


@dataclass
class Vaga:
    nome: str
    link: str
    status: VagaStatus
    id: Optional[int] = None
    data_aplicacao: Optional[str] = None
    descricao: Optional[str] = None
    empresa: Optional[Empresa] = None


def dictionary_to_vaga(data: dict) -> Vaga:
    """
    Converte um dicionário em uma instância de Vaga.
    """
    # Verificar se há dados de empresa
    empresa = None
    if data.get("nome_empresa"):
        empresa = Empresa(
            nome=data.get("nome_empresa"),
            id=data.get("id_empresa"),
            site=data.get("site_empresa"),
            setor=data.get("setor_empresa"),
        )

    return Vaga(
        nome=data.get("nome"),
        link=data.get("link"),
        status=data.get("status"),
        id=data.get("id"),
        data_aplicacao=data.get("data_aplicacao"),
        descricao=data.get("descricao"),
        empresa=empresa,
    )


def vaga_to_dictionary(vaga: Vaga) -> dict:
    """
    Converte uma instância de Vaga em um dicionário.
    """
    return {
        "id": vaga.id,
        "nome": vaga.nome,
        "link": vaga.link,
        "status": vaga.status.value,
        "data_aplicacao": vaga.data_aplicacao,
        "descricao": vaga.descricao,
        "id_empresa": vaga.empresa.id if vaga.empresa and vaga.empresa.id else None,
        "nome_empresa": vaga.empresa.nome
        if vaga.empresa and vaga.empresa.nome
        else None,
        "site_empresa": vaga.empresa.site
        if vaga.empresa and vaga.empresa.site
        else None,
        "setor_empresa": vaga.empresa.setor
        if vaga.empresa and vaga.empresa.setor
        else None,
    }
