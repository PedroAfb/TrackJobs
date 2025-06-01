from trackJobs.exceptions import ErroCandidaturaException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.repositories.SQLite.base_repository import BaseSQLiteRepository


class SQLiteVagaRepository(BaseSQLiteRepository):
    def listar_campos_vaga(self) -> list[str]:
        """Retorna os campos necessários para cadastro de vaga"""
        with self.transaction() as cursor:
            cursor.execute("PRAGMA table_info(vagas)")
            colunas_vagas = [row[1] for row in cursor.fetchall()]

        colunas_vagas.remove("id")
        colunas_vagas.remove("idEmpresa")

        return colunas_vagas

    def cadastrar_candidatura(self, candidatura: Vaga) -> None:
        """Cadastra uma nova candidatura no banco de dados"""
        with self.transaction() as cursor:
            msg_insert_candidatura = """
            INSERT INTO vagas
            (nome, link, status, descriçao, data_aplicaçao, idEmpresa) VALUES
            (?, ?, ?, ?, ?, ?)"""

            cursor.execute(
                msg_insert_candidatura,
                (
                    candidatura.vaga.nome,
                    candidatura.vaga.link,
                    candidatura.vaga.status,
                    candidatura.vaga.descricao,
                    candidatura.vaga.data_aplicacao,
                    candidatura.empresa.id if candidatura.empresa else None,
                ),
            )

    def buscar_vaga_por_link(self, link: str) -> Vaga:
        """Busca uma vaga pelo link"""
        with self.transaction() as cursor:
            cursor.execute(
                """SELECT id, nome, link, status, descricao, data_aplicacao, id_empresa
                FROM vagas WHERE link = ?""",
                (link,),
            )
            row = cursor.fetchone()

        if not row:
            raise ErroCandidaturaException("Vaga não encontrada.")

        vaga = Vaga(
            id=row[0],
            nome=row[1],
            link=row[2],
            status=row[3],
            descricao=row[4],
            data_aplicacao=row[5],
            id_empresa=row[6] if row[6] is not None else None,
        )
        return vaga
