from trackJobs.model.entities.empresa import Empresa
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
                """SELECT
                v.id, v.nome, v.link, v.status, v.descricao, v.data_aplicacao,
                e.id, e.nome, e.site, e.setor
                FROM vagas v
                LEFT JOIN empresas e ON v.idEmpresa = e.id
                WHERE link = ?""",
                (link,),
            )
            row = cursor.fetchone()

        if not row:
            return None

        empresa = None
        if row[6] is not None:
            empresa = Empresa(
                id=row[6],
                nome=row[7],
                site=row[8] if row[8] else None,
                setor=row[9] if row[9] else None,
            )

        vaga = Vaga(
            id=row[0],
            nome=row[1],
            link=row[2],
            status=row[3],
            descricao=row[4],
            data_aplicacao=row[5],
            empresa=empresa,
        )
        return vaga
