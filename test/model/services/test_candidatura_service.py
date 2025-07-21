from unittest.mock import Mock

from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.services.candidatura_service import CandidaturaService


class TestCandidaturaService:
    """Testes unitários para o CandidaturaService"""

    def setup_method(self):
        """Setup para cada teste - cria mocks para os repositories"""
        self.empresa_repository_mock = Mock()
        self.vaga_repository_mock = Mock()
        self.service = CandidaturaService(
            self.empresa_repository_mock, self.vaga_repository_mock
        )

    def test_filtra_vagas_por_nome(self):
        """Testa filtro de vagas por nome"""
        # Arrange
        vaga1 = Vaga(
            nome="Desenvolvedor Python", link="https://example.com/1", status="aplicado"
        )
        vaga2 = Vaga(
            nome="Analista Python", link="https://example.com/2", status="entrevista"
        )
        self.vaga_repository_mock.get_vaga_com_filtro.return_value = [vaga1, vaga2]

        # Act
        resultado = self.service.filtra_vagas("Python", "nome")

        # Assert
        assert len(resultado) == 2
        assert resultado[0].nome == "Desenvolvedor Python"
        assert resultado[1].nome == "Analista Python"
        self.vaga_repository_mock.get_vaga_com_filtro.assert_called_once_with(
            "Python", "nome"
        )

    def test_filtra_vagas_por_status(self):
        """Testa filtro de vagas por status"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/1", status="entrevista"
        )
        self.vaga_repository_mock.get_vaga_com_filtro.return_value = [vaga]

        # Act
        resultado = self.service.filtra_vagas("entrevista", "status")

        # Assert
        assert len(resultado) == 1
        assert resultado[0].status == "entrevista"
        self.vaga_repository_mock.get_vaga_com_filtro.assert_called_once_with(
            "entrevista", "status"
        )

    def test_filtra_vagas_sem_filtro(self):
        """Testa listagem de todas as vagas (sem filtro)"""
        # Arrange
        vaga1 = Vaga(nome="Dev Python", link="https://example.com/1", status="aplicado")
        vaga2 = Vaga(nome="Dev Java", link="https://example.com/2", status="entrevista")
        self.vaga_repository_mock.get_vaga_com_filtro.return_value = [vaga1, vaga2]

        # Act
        resultado = self.service.filtra_vagas()

        # Assert
        assert len(resultado) == 2
        self.vaga_repository_mock.get_vaga_com_filtro.assert_called_once_with("", "")

    def test_get_vaga_por_link_existente(self):
        """Testa busca de vaga por link existente"""
        # Arrange
        empresa = Empresa(id=1, nome="TechCorp", site="https://techcorp.com")
        vaga = Vaga(
            id=1,
            nome="Dev Python",
            link="https://example.com/vaga",
            status="aplicado",
            empresa=empresa,
        )
        self.vaga_repository_mock.buscar_vaga_por_link.return_value = vaga

        # Act
        resultado = self.service.get_vaga_por_link("https://example.com/vaga")

        # Assert
        assert resultado.nome == "Dev Python"
        assert resultado.empresa.nome == "TechCorp"
        self.vaga_repository_mock.buscar_vaga_por_link.assert_called_once_with(
            "https://example.com/vaga"
        )

    def test_get_vaga_por_link_inexistente(self):
        """Testa busca de vaga por link inexistente"""
        # Arrange
        self.vaga_repository_mock.buscar_vaga_por_link.return_value = None

        # Act
        resultado = self.service.get_vaga_por_link("https://link-inexistente.com")

        # Assert
        assert resultado is None
        self.vaga_repository_mock.buscar_vaga_por_link.assert_called_once_with(
            "https://link-inexistente.com"
        )

    def test_filtra_vagas_resultado_vazio(self):
        """Testa filtro que retorna resultado vazio"""
        # Arrange
        self.vaga_repository_mock.get_vaga_com_filtro.return_value = []

        # Act
        resultado = self.service.filtra_vagas("termo_inexistente", "nome")

        # Assert
        assert resultado == []
        self.vaga_repository_mock.get_vaga_com_filtro.assert_called_once_with(
            "termo_inexistente", "nome"
        )

    def test_filtra_vagas_com_empresa_associada(self):
        """Testa filtro de vagas que têm empresa associada"""
        # Arrange
        empresa = Empresa(
            id=1, nome="TechCorp", site="https://techcorp.com", setor="Tecnologia"
        )
        vaga = Vaga(
            nome="Dev Python",
            link="https://example.com/vaga",
            status="aplicado",
            empresa=empresa,
        )
        self.vaga_repository_mock.get_vaga_com_filtro.return_value = [vaga]

        # Act
        resultado = self.service.filtra_vagas("TechCorp", "empresa")

        # Assert
        assert len(resultado) == 1
        assert resultado[0].empresa.nome == "TechCorp"
        self.vaga_repository_mock.get_vaga_com_filtro.assert_called_once_with(
            "TechCorp", "empresa"
        )

    def test_get_vaga_por_link_string_vazia(self):
        """Testa busca de vaga com link vazio"""
        # Arrange
        self.vaga_repository_mock.buscar_vaga_por_link.return_value = None

        # Act
        resultado = self.service.get_vaga_por_link("")

        # Assert
        assert resultado is None
        self.vaga_repository_mock.buscar_vaga_por_link.assert_called_once_with("")

    def test_filtra_vagas_com_filtro_especial(self):
        """Testa filtro com caracteres especiais"""
        # Arrange
        vaga = Vaga(nome="Dev C#", link="https://example.com/vaga", status="aplicado")
        self.vaga_repository_mock.get_vaga_com_filtro.return_value = [vaga]

        # Act
        resultado = self.service.filtra_vagas("C#", "nome")

        # Assert
        assert len(resultado) == 1
        assert "C#" in resultado[0].nome
        self.vaga_repository_mock.get_vaga_com_filtro.assert_called_once_with(
            "C#", "nome"
        )
