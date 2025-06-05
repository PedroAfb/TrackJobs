from trackJobs.model.entities.empresa import dictionary_to_empresa
from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.empresa import empresa_to_dictionary


def test_dictionary_to_empresa_completo():
    """Testa conversão de dicionário para Empresa com todos os campos"""
    # Arrange
    dados = {
        "id_empresa": 1,
        "nome_empresa": "TechCorp",
        "site_empresa": "https://techcorp.com",
        "setor_empresa": "Tecnologia",
    }

    # Act
    empresa = dictionary_to_empresa(dados)

    # Assert
    assert isinstance(empresa, Empresa)
    assert empresa.id == 1
    assert empresa.nome == "TechCorp"
    assert empresa.site == "https://techcorp.com"
    assert empresa.setor == "Tecnologia"


def test_dictionary_to_empresa_apenas_nome():
    """Testa conversão de dicionário para Empresa apenas com nome"""
    # Arrange
    dados = {"nome_empresa": "TechCorp"}

    # Act
    empresa = dictionary_to_empresa(dados)

    # Assert
    assert isinstance(empresa, Empresa)
    assert empresa.nome == "TechCorp"
    assert empresa.id is None
    assert empresa.site is None
    assert empresa.setor is None


def test_empresa_to_dictionary_completo():
    """Testa conversão de Empresa para dicionário com todos os campos"""
    # Arrange
    empresa = Empresa(
        id=1, nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
    )

    # Act
    dados = empresa_to_dictionary(empresa)

    # Assert
    assert isinstance(dados, dict)
    assert dados["id_empresa"] == 1
    assert dados["nome_empresa"] == "TechCorp"
    assert dados["site_empresa"] == "https://techcorp.com"
    assert dados["setor_empresa"] == "Tecnologia"


def test_empresa_to_dictionary_apenas_nome():
    """Testa conversão de Empresa para dicionário apenas com nome"""
    # Arrange
    empresa = Empresa(nome="TechCorp")

    # Act
    dados = empresa_to_dictionary(empresa)

    # Assert
    assert isinstance(dados, dict)
    assert dados["nome_empresa"] == "TechCorp"
    assert dados["id_empresa"] is None
    assert dados["site_empresa"] is None
    assert dados["setor_empresa"] is None
