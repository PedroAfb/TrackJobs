from dataclasses import dataclass
from typing import Optional


@dataclass
class Empresa:
    nome: str
    id: Optional[int] = None
    site: Optional[str] = None
    setor: Optional[str] = None


def dictionary_to_empresa(data: dict) -> Empresa:
    """
    Converte um dicionário em uma instância de Empresa.
    """
    return Empresa(
        nome=data.get("nome_empresa"),
        id=data.get("id_empresa"),
        site=data.get("site_empresa"),
        setor=data.get("setor_empresa"),
    )


def empresa_to_dictionary(empresa: Empresa) -> dict:
    """
    Converte uma instância de Empresa em um dicionário.
    """
    return {
        "id_empresa": empresa.id,
        "nome_empresa": empresa.nome,
        "site_empresa": empresa.site,
        "setor_empresa": empresa.setor,
    }
