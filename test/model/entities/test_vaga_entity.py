from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.vaga import dictionary_to_vaga
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.entities.vaga import vaga_to_dictionary


def test_dictionary_to_vaga_completo_com_empresa():
    """Testa conversão de dicionário para Vaga com todos os campos e empresa"""
    # Arrange
    dados = {
        "id": 1,
        "nome": "Desenvolvedor Python",
        "link": "https://example.com/vaga",
        "status": "candidatar-se",
        "descricao": "Vaga para desenvolvedor Python",
        "data_aplicacao": "2025-06-01",
        "id_empresa": 2,
        "nome_empresa": "TechCorp",
        "site_empresa": "https://techcorp.com",
        "setor_empresa": "Tecnologia",
    }

    # Act
    vaga = dictionary_to_vaga(dados)

    # Assert
    assert isinstance(vaga, Vaga)
    assert vaga.id == 1
    assert vaga.nome == "Desenvolvedor Python"
    assert vaga.link == "https://example.com/vaga"
    assert vaga.status == "candidatar-se"
    assert vaga.descricao == "Vaga para desenvolvedor Python"
    assert vaga.data_aplicacao == "2025-06-01"

    # Verificar empresa
    assert vaga.empresa is not None
    assert vaga.empresa.id == 2
    assert vaga.empresa.nome == "TechCorp"
    assert vaga.empresa.site == "https://techcorp.com"
    assert vaga.empresa.setor == "Tecnologia"


def test_dictionary_to_vaga_sem_empresa():
    """Testa conversão de dicionário para Vaga sem empresa"""
    # Arrange
    dados = {
        "id": 1,
        "nome": "Desenvolvedor Python",
        "link": "https://example.com/vaga",
        "status": "candidatar-se",
        "descricao": "Vaga para desenvolvedor Python",
        "data_aplicacao": "2025-06-01",
    }

    # Act
    vaga = dictionary_to_vaga(dados)

    # Assert
    assert isinstance(vaga, Vaga)
    assert vaga.empresa is None


def test_dictionary_to_vaga_campos_minimos():
    """Testa conversão de dicionário para Vaga apenas com campos obrigatórios"""
    # Arrange
    dados = {
        "nome": "Desenvolvedor Python",
        "link": "https://example.com/vaga",
        "status": "candidatar-se",
    }

    # Act
    vaga = dictionary_to_vaga(dados)

    # Assert
    assert isinstance(vaga, Vaga)
    assert vaga.nome == "Desenvolvedor Python"
    assert vaga.link == "https://example.com/vaga"
    assert vaga.status == "candidatar-se"
    assert vaga.id is None
    assert vaga.descricao is None
    assert vaga.data_aplicacao is None
    assert vaga.empresa is None


def test_vaga_to_dictionary_completo_com_empresa():
    """Testa conversão de Vaga para dicionário com todos os campos e empresa"""
    # Arrange
    empresa = Empresa(
        id=2, nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
    )
    vaga = Vaga(
        id=1,
        nome="Desenvolvedor Python",
        link="https://example.com/vaga",
        status="candidatar-se",
        descricao="Vaga para desenvolvedor Python",
        data_aplicacao="2025-06-01",
        empresa=empresa,
    )

    # Act
    dados = vaga_to_dictionary(vaga)

    # Assert
    assert isinstance(dados, dict)
    assert dados["id"] == 1
    assert dados["nome"] == "Desenvolvedor Python"
    assert dados["link"] == "https://example.com/vaga"
    assert dados["status"] == "candidatar-se"
    assert dados["descricao"] == "Vaga para desenvolvedor Python"
    assert dados["data_aplicacao"] == "2025-06-01"

    # Verificar empresa
    assert dados["id_empresa"] == 2
    assert dados["nome_empresa"] == "TechCorp"
    assert dados["site_empresa"] == "https://techcorp.com"
    assert dados["setor_empresa"] == "Tecnologia"


def test_vaga_to_dictionary_sem_empresa():
    """Testa conversão de Vaga para dicionário sem empresa"""
    # Arrange
    vaga = Vaga(
        id=1,
        nome="Desenvolvedor Python",
        link="https://example.com/vaga",
        status="candidatar-se",
        descricao="Vaga para desenvolvedor Python",
        data_aplicacao="2025-06-01",
    )

    # Act
    dados = vaga_to_dictionary(vaga)

    # Assert
    assert isinstance(dados, dict)
    assert dados["id_empresa"] is None
    assert dados["nome_empresa"] is None
    assert dados["site_empresa"] is None
    assert dados["setor_empresa"] is None
