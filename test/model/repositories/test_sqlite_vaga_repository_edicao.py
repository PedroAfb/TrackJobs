from unittest.mock import Mock
from unittest.mock import patch

import pytest

from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.repositories.SQLite.sqlite_vaga_repository import (
    SQLiteVagaRepository,
)


class TestSQLiteVagaRepositoryEdicao:
    """Testes unitários para métodos de edição do SQLiteVagaRepository"""

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

        self.vaga_repository = SQLiteVagaRepository(self.db_mock)

    def teardown_method(self):
        """Cleanup após cada teste"""
        self.transaction_patch.stop()

    def test_atualizar_vaga_nome(self):
        """Testa atualização do nome da vaga"""
        # Arrange
        vaga = Vaga(
            id=1,
            nome="Dev Python",
            link="https://example.com/vaga",
            status="aplicado",
            descricao="Vaga para desenvolvedor",
        )

        # Act
        self.vaga_repository.atualizar_vaga(vaga, "nome", "Senior Python Developer")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "UPDATE vagas" in sql_call[0]
        assert "SET nome = ?" in sql_call[0]
        assert "WHERE link = ?" in sql_call[0]
        assert sql_call[1] == ("Senior Python Developer", "https://example.com/vaga")

    def test_atualizar_vaga_status(self):
        """Testa atualização do status da vaga"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )

        # Act
        self.vaga_repository.atualizar_vaga(vaga, "status", "entrevista")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "UPDATE vagas" in sql_call[0]
        assert "SET status = ?" in sql_call[0]
        assert sql_call[1] == ("entrevista", "https://example.com/vaga")

    def test_atualizar_vaga_descricao(self):
        """Testa atualização da descrição da vaga"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python",
            link="https://example.com/vaga",
            status="aplicado",
            descricao="Descrição antiga",
        )

        # Act
        self.vaga_repository.atualizar_vaga(vaga, "descricao", "Nova descrição da vaga")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "SET descricao = ?" in sql_call[0]
        assert sql_call[1] == ("Nova descrição da vaga", "https://example.com/vaga")

    def test_atualizar_vaga_data_aplicacao(self):
        """Testa atualização da data de aplicação"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python",
            link="https://example.com/vaga",
            status="aplicado",
            data_aplicacao="2025-07-20",
        )

        # Act
        self.vaga_repository.atualizar_vaga(vaga, "data_aplicacao", "2025-08-15")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "SET data_aplicacao = ?" in sql_call[0]
        assert sql_call[1] == ("2025-08-15", "https://example.com/vaga")

    def test_atualizar_vaga_link(self):
        """Testa atualização do link da vaga"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga-antiga", status="aplicado"
        )

        # Act
        self.vaga_repository.atualizar_vaga(
            vaga, "link", "https://example.com/vaga-nova"
        )

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "SET link = ?" in sql_call[0]
        assert sql_call[1] == (
            "https://example.com/vaga-nova",
            "https://example.com/vaga-antiga",
        )

    def test_get_vaga_com_filtro_por_nome(self):
        """Testa filtro de vagas por nome"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (
                1,
                "desenvolvedor python",
                "https://example.com/1",
                "aplicado",
                "Desc 1",
                "2025-07-21",
                1,
                "TechCorp",
                "https://techcorp.com",
                "Tecnologia",
            ),
            (
                2,
                "analista python",
                "https://example.com/2",
                "entrevista",
                "Desc 2",
                "2025-07-22",
                1,
                "TechCorp",
                "https://techcorp.com",
                "Tecnologia",
            ),
        ]

        # Act
        vagas = self.vaga_repository.get_vaga_com_filtro("python", "nome")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "WHERE v.nome LIKE ?" in sql_call[0]
        assert sql_call[1] == ["%python%"]
        assert len(vagas) == 2
        assert vagas[0].nome == "desenvolvedor python"
        assert vagas[1].nome == "analista python"

    def test_get_vaga_com_filtro_por_status(self):
        """Testa filtro de vagas por status"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (
                1,
                "dev python",
                "https://example.com/1",
                "entrevista",
                "Desc",
                "2025-07-21",
                None,
                None,
                None,
                None,
            ),
        ]

        # Act
        vagas = self.vaga_repository.get_vaga_com_filtro("entrevista", "status")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert "WHERE v.status LIKE ?" in sql_call[0]
        assert sql_call[1] == ["%entrevista%"]
        assert len(vagas) == 1
        assert vagas[0].status == "entrevista"

    def test_get_vaga_com_filtro_sem_filtro(self):
        """Testa listagem de todas as vagas (sem filtro)"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (
                1,
                "dev python",
                "https://example.com/1",
                "aplicado",
                "Desc 1",
                "2025-07-21",
                1,
                "TechCorp",
                "https://techcorp.com",
                "Tecnologia",
            ),
            (
                2,
                "dev java",
                "https://example.com/2",
                "entrevista",
                "Desc 2",
                "2025-07-22",
                1,
                "TechCorp",
                "https://techcorp.com",
                "Tecnologia",
            ),
        ]

        # Act
        vagas = self.vaga_repository.get_vaga_com_filtro("", "")

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        # Não deve ter WHERE na query quando não há filtro
        assert "WHERE" not in sql_call[0]
        assert len(vagas) == 2

    def test_get_vaga_com_filtro_com_empresa(self):
        """Testa filtro de vagas que inclui dados da empresa"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (
                1,
                "dev python",
                "https://example.com/1",
                "aplicado",
                "Desc",
                "2025-07-21",
                1,
                "TechCorp",
                "https://techcorp.com",
                "Tecnologia",
            ),
        ]

        # Act
        vagas = self.vaga_repository.get_vaga_com_filtro("python", "nome")

        # Assert
        assert len(vagas) == 1
        assert vagas[0].empresa is not None
        assert vagas[0].empresa.nome == "TechCorp"
        assert vagas[0].empresa.site == "https://techcorp.com"
        assert vagas[0].empresa.setor == "Tecnologia"

    def test_get_vaga_com_filtro_sem_empresa(self):
        """Testa filtro de vagas sem empresa associada"""
        # Arrange
        self.cursor_mock.fetchall.return_value = [
            (
                1,
                "dev python",
                "https://example.com/1",
                "aplicado",
                "Desc",
                "2025-07-21",
                None,
                None,
                None,
                None,
            ),
        ]

        # Act
        vagas = self.vaga_repository.get_vaga_com_filtro("python", "nome")

        # Assert
        assert len(vagas) == 1
        assert vagas[0].empresa is None

    def test_get_vaga_com_filtro_resultado_vazio(self):
        """Testa filtro que não retorna resultados"""
        # Arrange
        self.cursor_mock.fetchall.return_value = []

        # Act
        vagas = self.vaga_repository.get_vaga_com_filtro("termo_inexistente", "nome")

        # Assert
        assert len(vagas) == 0

    @pytest.mark.parametrize(
        "campo,valor_novo",
        [
            ("nome", "Senior Python Developer"),
            ("status", "rejeitado"),
            ("descricao", "Descrição atualizada"),
            ("data_aplicacao", "2025-12-25"),
            ("link", "https://novo-link.com/vaga"),
        ],
    )
    def test_atualizar_vaga_diferentes_campos(self, campo, valor_novo):
        """Testa atualização de diferentes campos"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )

        # Act
        self.vaga_repository.atualizar_vaga(vaga, campo, valor_novo)

        # Assert
        self.cursor_mock.execute.assert_called_once()
        sql_call = self.cursor_mock.execute.call_args[0]
        assert f"SET {campo} = ?" in sql_call[0]
        assert sql_call[1] == (valor_novo, "https://example.com/vaga")

    def test_buscar_vaga_por_link_existente_com_empresa(self):
        """Testa busca de vaga por link com empresa associada"""
        # Arrange
        self.cursor_mock.fetchone.return_value = (
            1,
            "dev python",
            "https://example.com/vaga",
            "aplicado",
            "Descrição",
            "2025-07-21",
            1,
            "TechCorp",
            "https://techcorp.com",
            "Tecnologia",
        )

        # Act
        vaga = self.vaga_repository.buscar_vaga_por_link("https://example.com/vaga")

        # Assert
        assert vaga is not None
        assert vaga.nome == "dev python"
        assert vaga.empresa.nome == "TechCorp"
        self.cursor_mock.execute.assert_called_once_with(
            """SELECT
                v.id, v.nome, v.link, v.status, v.descriçao, v.data_aplicaçao,
                e.id, e.nome, e.site, e.setor
                FROM vagas v
                LEFT JOIN empresas e ON v.idEmpresa = e.id
                WHERE link = ?""",
            ("https://example.com/vaga",),
        )

    def test_buscar_vaga_por_link_existente_sem_empresa(self):
        """Testa busca de vaga por link sem empresa associada"""
        # Arrange
        self.cursor_mock.fetchone.return_value = (
            1,
            "dev python",
            "https://example.com/vaga",
            "aplicado",
            "Descrição",
            "2025-07-21",
            None,
            None,
            None,
            None,
        )

        # Act
        vaga = self.vaga_repository.buscar_vaga_por_link("https://example.com/vaga")

        # Assert
        assert vaga is not None
        assert vaga.nome == "dev python"
        assert vaga.empresa is None

    def test_buscar_vaga_por_link_inexistente(self):
        """Testa busca de vaga por link que não existe"""
        # Arrange
        self.cursor_mock.fetchone.return_value = None

        # Act
        vaga = self.vaga_repository.buscar_vaga_por_link("https://link-inexistente.com")

        # Assert
        assert vaga is None
        self.cursor_mock.execute.assert_called_once()
