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
                    vaga.nome.lower(),
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
                v.id, v.nome, v.link, v.status, v.descriçao, v.data_aplicaçao,
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

    def get_vaga_com_filtro(
        self, filtro: str = "", tipo_filtro: str = ""
    ) -> list[Vaga]:
        """Busca vagas com base em um filtro"""

        query = """
            SELECT
            v.id, v.nome, v.link, v.status, v.descriçao, v.data_aplicaçao,
            e.id, e.nome, e.site, e.setor
            FROM vagas v
            LEFT JOIN empresas e ON v.idEmpresa = e.id
        """
        params = []
        if tipo_filtro in ["link", "nome", "status"]:
            query += f" WHERE {tipo_filtro} LIKE ?"
            params.append(f"%{filtro}%")

        with self.base_repository.transaction() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return [
            Vaga(
                id=row[0],
                nome=row[1],
                link=row[2],
                status=row[3],
                descricao=row[4],
                data_aplicacao=row[5],
                empresa=Empresa(
                    id=row[6],
                    nome=row[7],
                    site=row[8] if row[8] else None,
                    setor=row[9] if row[9] else None,
                )
                if row[6] is not None
                else None,
            )
            for row in rows
        ]

    def atualizar_vaga(self, vaga: Vaga, campo_update: str, novo_dado: str) -> None:
        """Atualiza uma vaga existente no banco de dados"""
        with self.base_repository.transaction() as cursor:
            msg_update_vaga = f"""
            UPDATE vagas
            SET {campo_update} = ?
            WHERE link = ?"""

            cursor.execute(
                msg_update_vaga,
                (
                    novo_dado,
                    vaga.link,
                ),
            )
