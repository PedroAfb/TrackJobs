from trackJobs.exceptions import ErroCandidaturaException
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.repositories.interfaces.vaga_repository import VagaRepository
from trackJobs.model.repositories.SQLite.base_repository import BaseSQLiteRepository


class SQLiteVagaRepository(VagaRepository):
    def __init__(self, db):
        self.db = db
        self.base_repository = BaseSQLiteRepository(db)

    def listar_campos_vaga(self) -> list[str]:
        """Retorna os campos necessários para cadastro de vaga"""
        with self.base_repository.transaction() as cursor:
            cursor.execute("PRAGMA table_info(vagas)")
            colunas_vagas = [row[1] for row in cursor.fetchall()]

        colunas_vagas.remove("id")
        colunas_vagas.remove("idEmpresa")

        return colunas_vagas

    def cadastrar_candidatura(self, vaga: Vaga) -> None:
        """Cadastra uma nova candidatura no banco de dados"""
        with self.base_repository.transaction() as cursor:
            msg_insert_candidatura = """
            INSERT INTO vagas
            (nome, link, status, descriçao, data_aplicaçao, idEmpresa) VALUES
            (?, ?, ?, ?, ?, ?)"""

            cursor.execute(
                msg_insert_candidatura,
                (
                    vaga.nome,
                    vaga.link,
                    vaga.status,
                    vaga.descricao,
                    vaga.data_aplicacao,
                    vaga.empresa.id if vaga.empresa else None,
                ),
            )

    def buscar_vaga_por_link(self, link: str) -> Vaga:
        """Busca uma vaga pelo link"""
        with self.base_repository.transaction() as cursor:
            cursor.execute(
                """SELECT id, nome, link, status, descriçao, data_aplicaçao, idEmpresa
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
