from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel

from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.vaga import Vaga


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Union[Vaga, Empresa, List[Vaga], List[Empresa]]] = None
