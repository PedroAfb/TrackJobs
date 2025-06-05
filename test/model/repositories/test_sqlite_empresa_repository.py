from unittest.mock import Mock
from unittest.mock import patch

from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.repositories.SQLite.sqlite_empresa_repository import (
    SQLiteEmpresaRepository,
)


class TestSQLiteEmpresaRepository:
    """Testes unitários para o SQLiteEmpresaRepository"""

    def setup_method(self):
        """Setup para cada teste - cria mock para o banco de dados"""
        self.db_mock = Mock()
        self.cursor_mock = Mock()
        self.db_mock.cursor = self.cursor_mock
        self.db_mock.conexao = Mock()

        # Mock do BaseSQLiteRepository.transaction
        self.transaction_patch = patch(
            "trackJobs.model.repositories."
            "SQLite.base_repository.BaseSQLiteRepository.transaction"
        )
        self.transaction_mock = self.transaction_patch.start()
        # Configura o transaction para retornar o cursor_mock no contexto
        self.transaction_mock.return_value.__enter__.return_value = self.cursor_mock

        self.empresa_repository = SQLiteEmpresaRepository(self.db_mock)

    def teardown_method(self):
        """Cleanup após cada teste"""
        self.transaction_patch.stop()

    def test_listar_campos_empresa(self):
        """Testa listagem de campos da empresa"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (0, "id", "", 0, None, 0),
            (1, "nome", "", 0, None, 0),
            (2, "site", "", 0, None, 0),
            (3, "setor", "", 0, None, 0),
        ]

        # Act
        campos = self.empresa_repository.listar_campos_empresa()

        # Assert
        self.cursor_mock.execute.assert_called_once_with("PRAGMA table_info(empresas)")
        assert campos == ["nome_empresa", "site_empresa", "setor_empresa"]

    def test_cadastrar_empresa(self):
        """Testa cadastro de empresa"""
        # Arrange
        empresa = Empresa(
            nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
        )
        self.cursor_mock.lastrowid = 1

        # Act
        empresa_cadastrada = self.empresa_repository.cadastrar_empresa(empresa)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        assert "INSERT INTO empresas" in self.cursor_mock.execute.call_args[0][0]
        assert self.cursor_mock.execute.call_args[0][1] == (
            "techcorp",
            "https://techcorp.com",
            "tecnologia",
        )
        assert empresa_cadastrada.id == 1
        assert empresa_cadastrada == empresa

    def test_cadastrar_empresa_sem_site_e_setor(self):
        """Testa cadastro de empresa sem site e setor"""
        # Arrange
        empresa = Empresa(nome="TechCorp")
        self.cursor_mock.lastrowid = 1

        # Act
        empresa_cadastrada = self.empresa_repository.cadastrar_empresa(empresa)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        assert self.cursor_mock.execute.call_args[0][1] == ("techcorp", None, None)
        assert empresa_cadastrada.id == 1
        assert empresa_cadastrada == empresa

    def test_listar_nome_empresas(self):
        """Testa listagem de nomes de empresas"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            ("techcorp",),
            ("google",),
            ("microsoft",),
        ]

        # Act
        empresas = self.empresa_repository.listar_nome_empresas()

        # Assert
        self.cursor_mock.execute.assert_called_once_with(
            "SELECT nome FROM empresas ORDER BY nome"
        )
        assert empresas == ["Techcorp", "Google", "Microsoft"]

    def test_buscar_empresa_por_nome_existente(self):
        """Testa busca de empresa por nome existente"""
        # Arrange
        self.cursor_mock.fetchone.return_value = (
            1,
            "techcorp",
            "https://techcorp.com",
            "Tecnologia",
        )
        nome_empresa = "TechCorp"

        # Act
        empresa = self.empresa_repository.buscar_empresa_por_nome(nome_empresa)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        assert (
            "SELECT id, nome, site, setor" in self.cursor_mock.execute.call_args[0][0]
        )
        assert self.cursor_mock.execute.call_args[0][1] == ("techcorp",)
        assert isinstance(empresa, Empresa)
        assert empresa.id == 1
        assert empresa.nome == "techcorp"
        assert empresa.site == "https://techcorp.com"
        assert empresa.setor == "Tecnologia"

    def test_buscar_empresa_por_nome_inexistente(self):
        """Testa busca de empresa por nome inexistente"""
        # Arrange
        self.cursor_mock.fetchone.return_value = None

        # Act
        empresa = self.empresa_repository.buscar_empresa_por_nome("Inexistente")

        # Assert
        assert empresa is None

    def test_buscar_empresa_por_nome_vazio(self):
        """Testa busca de empresa por nome vazio"""
        # Act
        empresa = self.empresa_repository.buscar_empresa_por_nome("")

        # Assert
        self.cursor_mock.execute.assert_not_called()
        assert empresa is None

    def test_buscar_empresa_por_link_existente(self):
        """Testa busca de empresa por link existente"""
        # Arrange
        self.cursor_mock.fetchone.return_value = (
            1,
            "techcorp",
            "https://techcorp.com",
            "Tecnologia",
        )

        # Act
        empresa = self.empresa_repository.buscar_empresa_por_link(
            "https://techcorp.com"
        )

        # Assert
        self.cursor_mock.execute.assert_called_once()
        assert (
            "SELECT id, nome, site, setor" in self.cursor_mock.execute.call_args[0][0]
        )
        assert self.cursor_mock.execute.call_args[0][1] == ("https://techcorp.com",)
        assert empresa.id == 1
        assert empresa.nome == "techcorp"
        assert empresa.site == "https://techcorp.com"
        assert empresa.setor == "Tecnologia"

    def test_buscar_empresa_por_link_inexistente(self):
        """Testa busca de empresa por link inexistente"""
        # Arrange
        self.cursor_mock.fetchone.return_value = None

        # Act
        empresa = self.empresa_repository.buscar_empresa_por_link(
            "https://inexistente.com"
        )

        # Assert
        assert empresa is None

    def test_buscar_empresa_por_link_vazio(self):
        """Testa busca de empresa por link vazio"""
        # Act
        empresa = self.empresa_repository.buscar_empresa_por_link("")

        # Assert
        self.cursor_mock.execute.assert_not_called()
        assert empresa is None
