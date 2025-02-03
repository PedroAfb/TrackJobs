from .fixtures import dados_cadastro_sucesso_sem_empresa, dados_cadastro_sem_empresa_link_duplicado, dados_cadastro_sem_empresa_link_invalido
import pytest

@pytest.fixture
def dict_cadastro_sucesso_sem_empresa():
    return dados_cadastro_sucesso_sem_empresa

@pytest.fixture
def dict_cadastro_sem_empresa_link_duplicado():
    return dados_cadastro_sem_empresa_link_duplicado

@pytest.fixture
def dict_cadastro_sem_empresa_link_invalido():
    return dados_cadastro_sem_empresa_link_invalido
