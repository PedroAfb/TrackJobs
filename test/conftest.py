import pytest

from .fixtures import dados_cadastro_com_empresa
from .fixtures import dados_cadastro_com_empresa2
from .fixtures import dados_cadastro_sem_empresa_link_duplicado
from .fixtures import dados_cadastro_sem_empresa_link_invalido
from .fixtures import dados_cadastro_sucesso_sem_empresa


@pytest.fixture
def dict_cadastro_sucesso_sem_empresa():
    return dados_cadastro_sucesso_sem_empresa


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
