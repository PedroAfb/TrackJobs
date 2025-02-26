import pytest

from .fixtures import candidaturas_filtradas_por_link
from .fixtures import candidaturas_filtradas_por_nome
from .fixtures import candidaturas_filtradas_por_status
from .fixtures import dados_cadastro_com_empresa
from .fixtures import dados_cadastro_com_empresa2
from .fixtures import dados_cadastro_sem_empresa
from .fixtures import dados_cadastro_sem_empresa_link_duplicado
from .fixtures import dados_cadastro_sem_empresa_link_invalido
from .fixtures import dados_todas_candidaturas
from .fixtures import nenhum_candidatura_printada
from .fixtures import status_printado
from .fixtures import todas_candidaturas_printadas


@pytest.fixture
def dict_cadastro_sem_empresa():
    return dados_cadastro_sem_empresa


@pytest.fixture
def dict_cadastro_sem_empresa_link_duplicado():
    return dados_cadastro_sem_empresa_link_duplicado


@pytest.fixture
def dict_cadastro_sem_empresa_link_invalido():
    return dados_cadastro_sem_empresa_link_invalido


@pytest.fixture
def dict_cadastro_com_empresa():
    return dados_cadastro_com_empresa


@pytest.fixture
def dict_cadastro_com_empresa2():
    return dados_cadastro_com_empresa2


@pytest.fixture
def todas_candidaturas():
    return dados_todas_candidaturas


@pytest.fixture
def esperado_todas_candidaturas_printadas():
    return todas_candidaturas_printadas


@pytest.fixture
def esperado_candidaturas_filtradas_por_nome():
    return candidaturas_filtradas_por_nome


@pytest.fixture
def esperado_candidaturas_filtradas_por_link():
    return candidaturas_filtradas_por_link


@pytest.fixture
def esperado_candidaturas_filtradas_por_status():
    return candidaturas_filtradas_por_status


@pytest.fixture
def esperado_nenhuma_candidatura_printada():
    return nenhum_candidatura_printada


@pytest.fixture
def esperado_status_printado():
    return status_printado
