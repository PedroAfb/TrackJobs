from dataclasses import dataclass
from typing import Optional


@dataclass
class Empresa:
    id: int
    nome: str
    site: Optional[str] = None
    setor: Optional[str] = None
