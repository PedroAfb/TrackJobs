from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class VagaStatus(Enum):
    CANDIDATARSE = "Candidatar-se"
    EM_ANALISE = "Em análise"
    ENTREVISTA = "Entrevista"
    REJEITADO = "Rejeitado"
    ACEITO = "Aceito"


@dataclass
class Vaga:
    id: int
    nome: str
    link: str
    status: VagaStatus
    data_aplicacao: Optional[date] = None
    descricao: Optional[str] = None
