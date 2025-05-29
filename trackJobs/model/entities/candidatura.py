from dataclasses import dataclass
from typing import Optional

from .empresa import Empresa
from .vaga import Vaga


@dataclass
class Candidatura:
    vaga: Vaga
    empresa: Optional[Empresa] = None
