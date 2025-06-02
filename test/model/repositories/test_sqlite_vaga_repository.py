from unittest.mock import Mock
from unittest.mock import patch

from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.repositories.SQLite.sqlite_vaga_repository import (
    SQLiteVagaRepository,
)


class TestSQLiteVagaRepository:
    """Testes unitários para o SQLiteVagaRepository"""

    def setup_method(self):
        """Setup para cada teste - cria mock para o banco de dados"""
        self.db_mock = Mock()
        self.cursor_mock = Mock()
        self.db_mock.cursor = self.cursor_mock
        self.db_mock.conexao = Mock()

        # Mock do BaseSQLiteRepository.transaction
        self.transaction_patch = patch(
            """trackJobs.model.repositories.
            SQLite.base_repository.BaseSQLiteRepository.transaction"""
        )
        self.transaction_mock = self.transaction_patch.start()
        # Configura o transaction para retornar o cursor_mock no contexto
        self.transaction_mock.return_value.__enter__.return_value = self.cursor_mock

        self.vaga_repository = SQLiteVagaRepository(self.db_mock)

    def teardown_method(self):
        """Cleanup após cada teste"""
        self.transaction_patch.stop()

    def test_listar_campos_vaga(self):
        """Testa listagem de campos da vaga"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (0, "id", "", 0, None, 0),
            (1, "nome", "", 0, None, 0),
            (2, "link", "", 0, None, 0),
            (3, "status", "", 0, None, 0),
            (4, "descriçao", "", 0, None, 0),
            (5, "data_aplicaçao", "", 0, None, 0),
            (6, "idEmpresa", "", 0, None, 0),
        ]

        # Act
        campos = self.vaga_repository.listar_campos_vaga()

        # Assert
        self.cursor_mock.execute.assert_called_once_with("PRAGMA table_info(vagas)")
        assert "nome" in campos
        assert "link" in campos
        assert "status" in campos
        assert "descriçao" in campos
        assert "data_aplicaçao" in campos
        assert "id" not in campos
        assert "idEmpresa" not in campos

    def test_cadastrar_candidatura_com_empresa(self):
        """Testa cadastro de candidatura com empresa"""
        # Arrange
        empresa = Empresa(
            id=1, nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
        )
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            descricao="Vaga para desenvolvedor Python",
            data_aplicacao="2025-06-01",
            empresa=empresa,
        )

        # Act
        self.vaga_repository.cadastrar_candidatura(vaga)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        assert "INSERT INTO vagas" in self.cursor_mock.execute.call_args[0][0]
        params = self.cursor_mock.execute.call_args[0][1]
        assert params[0] == "Desenvolvedor Python"  # nome
        assert params[1] == "https://example.com/vaga"  # link
        assert params[2] == "candidatar-se"  # status
        assert params[3] == "Vaga para desenvolvedor Python"  # descrição
        assert params[4] == "2025-06-01"  # data_aplicacao
        assert params[5] == 1  # idEmpresa

    def test_cadastrar_candidatura_sem_empresa(self):
        """Testa cadastro de candidatura sem empresa"""
        # Arrange
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            descricao="Vaga para desenvolvedor Python",
            data_aplicacao="2025-06-01",
            empresa=None,
        )

        # Act
        self.vaga_repository.cadastrar_candidatura(vaga)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        params = self.cursor_mock.execute.call_args[0][1]
        assert params[5] is None  # idEmpresa deve ser None

    def test_cadastrar_candidatura_sem_descricao_e_data(self):
        """Testa cadastro de candidatura sem descrição e data"""
        # Arrange
        vaga = Vaga(
            nome="Desenvolvedor Python",
            link="https://example.com/vaga",
            status="candidatar-se",
            empresa=None,
        )

        # Act
        self.vaga_repository.cadastrar_candidatura(vaga)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        params = self.cursor_mock.execute.call_args[0][1]
        assert params[3] is None  # descrição
        assert params[4] is None  # data_aplicacao

    def test_buscar_vaga_por_link_existente(self):
        """Testa busca de vaga por link existente"""
        # Arrange
        self.cursor_mock.fetchone.return_value = (
            1,  # v.id
            "Desenvolvedor Python",  # v.nome
            "https://example.com/vaga",  # v.link
            "candidatar-se",  # v.status
            "Vaga para desenvolvedor Python",  # v.descricao
            "2025-06-01",  # v.data_aplicacao
            1,  # e.id
            "TechCorp",  # e.nome
            "https://techcorp.com",  # e.site
            "Tecnologia",  # e.setor
        )

        # Act
        vaga = self.vaga_repository.buscar_vaga_por_link("https://example.com/vaga")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        assert "SELECT " in self.cursor_mock.execute.call_args[0][0]
        assert "FROM vagas v" in self.cursor_mock.execute.call_args[0][0]
        assert "LEFT JOIN empresas e ON" in self.cursor_mock.execute.call_args[0][0]
        assert "WHERE link = ?" in self.cursor_mock.execute.call_args[0][0]
        assert self.cursor_mock.execute.call_args[0][1] == ("https://example.com/vaga",)

        # Verifica dados da vaga
        assert vaga.id == 1
        assert vaga.nome == "Desenvolvedor Python"
        assert vaga.link == "https://example.com/vaga"
        assert vaga.status == "candidatar-se"
        assert vaga.descricao == "Vaga para desenvolvedor Python"
        assert vaga.data_aplicacao == "2025-06-01"

        # Verifica dados da empresa
        assert vaga.empresa is not None
        assert vaga.empresa.id == 1
        assert vaga.empresa.nome == "TechCorp"
        assert vaga.empresa.site == "https://techcorp.com"
        assert vaga.empresa.setor == "Tecnologia"

    def test_buscar_vaga_por_link_inexistente(self):
        """Testa busca de vaga por link inexistente"""
        # Arrange
        self.cursor_mock.fetchone.return_value = None

        # Act
        vaga = self.vaga_repository.buscar_vaga_por_link("https://inexistente.com/vaga")

        # Assert
        assert vaga is None
        self.cursor_mock.execute.assert_called_once()

    def test_buscar_vaga_por_link_sem_empresa(self):
        """Testa busca de vaga por link sem empresa associada"""
        # Arrange
        self.cursor_mock.fetchone.return_value = (
            1,  # v.id
            "Desenvolvedor Python",  # v.nome
            "https://example.com/vaga",  # v.link
            "candidatar-se",  # v.status
            "Vaga para desenvolvedor Python",  # v.descricao
            "2025-06-01",  # v.data_aplicacao
            None,  # e.id (None)
            None,  # e.nome (None)
            None,  # e.site (None)
            None,  # e.setor (None)
        )

        # Act
        vaga = self.vaga_repository.buscar_vaga_por_link("https://example.com/vaga")

        # Assert
        assert vaga.empresa is None
        assert vaga.id == 1
        assert vaga.nome == "Desenvolvedor Python"
        assert vaga.link == "https://example.com/vaga"
        assert vaga.status == "candidatar-se"
        assert vaga.descricao == "Vaga para desenvolvedor Python"
        assert vaga.data_aplicacao == "2025-06-01"
