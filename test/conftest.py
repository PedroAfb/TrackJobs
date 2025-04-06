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
from .fixtures import mensagem_sucesso_edicao_data
from .fixtures import mensagem_sucesso_edicao_descricao
from .fixtures import mensagem_sucesso_edicao_link
from .fixtures import mensagem_sucesso_edicao_nome
from .fixtures import mensagem_sucesso_edicao_status
from .fixtures import mensagem_sucesso_remocao
from .fixtures import mensagem_sucesso_status
from .fixtures import nenhum_candidatura_printada
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
def esperado_mensagem_sucesso():
    return mensagem_sucesso_status


@pytest.fixture
def esperado_msg_edicao():
    return mensagem_sucesso_edicao_nome


@pytest.fixture
def esperado_msg_link():
    return mensagem_sucesso_edicao_link


@pytest.fixture
def esperado_msg_data():
    return mensagem_sucesso_edicao_data


@pytest.fixture
def esperado_msg_status():
    return mensagem_sucesso_edicao_status


@pytest.fixture
def esperado_msg_descricao():
    return mensagem_sucesso_edicao_descricao


@pytest.fixture
def esperado_msg_remocao_sucesso():
    return mensagem_sucesso_remocao
