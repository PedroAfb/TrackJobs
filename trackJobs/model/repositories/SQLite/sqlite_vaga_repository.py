from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.entities.vaga import Vaga
from trackJobs.model.entities.vaga import VagaQuery
from trackJobs.model.entities.vaga import VagaUpdate
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

    def cadastrar_candidatura(self, vaga: Vaga) -> int:
        """Cadastra uma nova candidatura no banco de dados"""
        with self.base_repository.transaction() as cursor:
            msg_insert_candidatura = """
            INSERT INTO vagas
            (nome, link, status, descricao, data_aplicacao, idEmpresa) VALUES
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

            vaga_id = cursor.lastrowid
        return vaga_id

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

    def get_vaga_com_filtro(
        self, filtro: str = "", tipo_filtro: str = ""
    ) -> list[Vaga]:
        """Busca vagas com base em um filtro"""

        query = """
            SELECT
            v.id, v.nome, v.link, v.status, v.descricao, v.data_aplicacao,
            e.id, e.nome, e.site, e.setor
            FROM vagas v
            LEFT JOIN empresas e ON v.idEmpresa = e.id
        """
        params = []
        if tipo_filtro in ["link", "nome", "status"]:
            query += f" WHERE v.{tipo_filtro} LIKE ?"
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

    def get_vaga(self, filtro: VagaQuery) -> list[Vaga]:
        """Busca vagas com base em um filtro"""

        query = """
            SELECT
            v.id, v.nome, v.link, v.status, v.descricao, v.data_aplicacao,
            e.id, e.nome, e.site, e.setor
            FROM vagas v
            LEFT JOIN empresas e ON v.idEmpresa = e.id
            WHERE 1=1
        """
        params = []
        if filtro.nome:
            query += " AND v.nome LIKE ?"
            params.append(f"%{filtro.nome}%")
        if filtro.link:
            query += " AND v.link LIKE ?"
            params.append(f"%{filtro.link}%")
        if filtro.status:
            query += " AND v.status LIKE ?"
            params.append(f"%{filtro.status}%")
        if filtro.descricao:
            query += " AND v.descricao LIKE ?"
            params.append(f"%{filtro.descricao}%")
        if filtro.id:
            query += " AND v.id = ?"
            params.append(filtro.id)

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

    def atualizar_campos_vaga(
        self, vaga: VagaUpdate, dados_update: dict
    ) -> Vaga | None:
        with self.base_repository.transaction() as cursor:
            set_clause = ", ".join(f"{campo} = ?" for campo in dados_update.keys())
            msg_update_vaga = f"""
            UPDATE vagas
            SET {set_clause}
            WHERE id = ?"""

            cursor.execute(
                msg_update_vaga,
                (*dados_update.values(), vaga.id),
            )

            vaga_atualizada = self.get_vaga(
                VagaQuery(id=vaga.id)
            )  # Recarrega a vaga atualizada
            return vaga_atualizada[0] if vaga_atualizada else None

    def remover_vaga(self, vaga: Vaga) -> None:
        """Remove uma vaga do banco de dados"""
        with self.base_repository.transaction() as cursor:
            msg_delete_vaga = "DELETE FROM vagas WHERE link = ?"
            cursor.execute(msg_delete_vaga, (vaga.link,))
