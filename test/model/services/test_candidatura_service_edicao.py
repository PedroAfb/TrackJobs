from unittest.mock import Mock

import pytest

from trackJobs.exceptions import CampoInvalidoException
from trackJobs.exceptions import TrackJobsException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.services.candidatura_service import CandidaturaService


class TestCandidaturaServiceEdicao:
    """Testes unitários para métodos de edição do CandidaturaService"""

    def setup_method(self):
        """Setup para cada teste"""
        self.empresa_repository_mock = Mock()
        self.vaga_repository_mock = Mock()
        self.service = CandidaturaService(
            self.empresa_repository_mock, self.vaga_repository_mock
        )

    def test_atualiza_vaga_campo_valido(self):
        """Testa atualização de vaga com campo válido"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = [
            "nome",
            "link",
            "status",
            "descricao",
        ]

        # Act
        self.service.atualiza_vaga(vaga, "status", "entrevista")

        # Assert
        self.vaga_repository_mock.listar_campos_vaga.assert_called_once()
        self.vaga_repository_mock.atualizar_vaga.assert_called_once_with(
            vaga, "status", "entrevista"
        )

    def test_atualiza_vaga_campo_invalido(self):
        """Testa atualização de vaga com campo inválido"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = [
            "nome",
            "link",
            "status",
            "descricao",
        ]

        # Act & Assert
        with pytest.raises(CampoInvalidoException) as exc_info:
            self.service.atualiza_vaga(vaga, "campo_inexistente", "valor")

        assert "campo_inexistente" in str(exc_info.value)
        assert "não é válido para atualização" in str(exc_info.value)
        self.vaga_repository_mock.atualizar_vaga.assert_not_called()

    @pytest.mark.parametrize(
        "campo,novo_valor",
        [
            ("nome", "Senior Python Developer"),
            ("status", "rejeitado"),
            ("descricao", "Nova descrição da vaga"),
            ("link", "https://nova-url.com/vaga"),
            ("data_aplicacao", "2025-08-15"),
        ],
    )
    def test_atualiza_vaga_diferentes_campos(self, campo, novo_valor):
        """Testa atualização de diferentes campos da vaga"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = [
            "nome",
            "link",
            "status",
            "descricao",
            "data_aplicacao",
        ]

        # Act
        self.service.atualiza_vaga(vaga, campo, novo_valor)

        # Assert
        self.vaga_repository_mock.atualizar_vaga.assert_called_once_with(
            vaga, campo, novo_valor
        )

    def test_atualiza_vaga_erro_no_repository(self):
        """Testa erro no repository durante atualização"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = [
            "nome",
            "link",
            "status",
        ]
        self.vaga_repository_mock.atualizar_vaga.side_effect = TrackJobsException(
            "Erro no banco de dados"
        )

        # Act & Assert
        with pytest.raises(TrackJobsException) as exc_info:
            self.service.atualiza_vaga(vaga, "status", "entrevista")

        assert "Erro no banco de dados" in str(exc_info.value)

    def test_atualiza_vaga_vaga_none(self):
        """Testa atualização com vaga None"""
        # Arrange
        self.vaga_repository_mock.listar_campos_vaga.return_value = ["nome", "status"]

        # Act
        self.service.atualiza_vaga(None, "status", "entrevista")

        # Assert
        self.vaga_repository_mock.atualizar_vaga.assert_called_once_with(
            None, "status", "entrevista"
        )

    def test_atualiza_vaga_campo_vazio(self):
        """Testa atualização com campo vazio"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = ["nome", "status"]

        # Act & Assert
        with pytest.raises(CampoInvalidoException) as exc_info:
            self.service.atualiza_vaga(vaga, "", "novo_valor")

        assert "não é válido para atualização" in str(exc_info.value)

    def test_atualiza_vaga_valor_vazio(self):
        """Testa atualização com valor vazio (deve ser permitido)"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = [
            "nome",
            "status",
            "descricao",
        ]

        # Act
        self.service.atualiza_vaga(vaga, "descricao", "")

        # Assert
        self.vaga_repository_mock.atualizar_vaga.assert_called_once_with(
            vaga, "descricao", ""
        )

    @pytest.mark.parametrize(
        "campo_invalido",
        ["campo_inexistente", "id", "empresa_id", "data_criacao", "usuario_id"],
    )
    def test_atualiza_vaga_campos_invalidos_parametrizado(self, campo_invalido):
        """Testa atualização com diferentes campos inválidos"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.return_value = [
            "nome",
            "link",
            "status",
            "descricao",
            "data_aplicacao",
        ]

        # Act & Assert
        with pytest.raises(CampoInvalidoException) as exc_info:
            self.service.atualiza_vaga(vaga, campo_invalido, "novo_valor")

        assert f"Campo '{campo_invalido}' não é válido para atualização" in str(
            exc_info.value
        )
        self.vaga_repository_mock.atualizar_vaga.assert_not_called()

    def test_atualiza_vaga_repositorio_indisponivel(self):
        """Testa atualização quando repository lança erro de conexão"""
        # Arrange
        vaga = Vaga(
            nome="Dev Python", link="https://example.com/vaga", status="aplicado"
        )
        self.vaga_repository_mock.listar_campos_vaga.side_effect = Exception(
            "Conexão perdida"
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.service.atualiza_vaga(vaga, "status", "entrevista")

        assert "Conexão perdida" in str(exc_info.value)
