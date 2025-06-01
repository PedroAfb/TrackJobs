from typing import Optional

from trackJobs.model.entities.empresa import Empresa
from trackJobs.model.repositories.interfaces.empresa_repository import EmpresaRepository
from trackJobs.model.repositories.SQLite.base_repository import BaseSQLiteRepository


class SQLiteEmpresaRepository(EmpresaRepository):
    def __init__(self, db):
        self.db = db
        self.base_repository = BaseSQLiteRepository(db)

    def listar_campos_empresa(self) -> list[str]:
        """Retorna os campos necessários para cadastro de empresa"""
        with self.base_repository.transaction() as cursor:
            cursor.execute("PRAGMA table_info(empresas)")
            colunas_empresas = [row[1] + "_empresa" for row in cursor.fetchall()]

        colunas_empresas.remove("id_empresa")
        return colunas_empresas

    def cadastrar_empresa(self, empresa: Empresa) -> int:
        """Cadastra uma nova empresa no banco de dados e retorna o id"""
        with self.base_repository.transaction() as cursor:
            msg_insert_empresas = """
                INSERT INTO empresas (nome, site, setor) VALUES
            (?, ?, ?)
            """
            cursor.execute(
                msg_insert_empresas,
                (
                    empresa.nome,
                    empresa.site if empresa.site else None,
                    empresa.setor if empresa.setor else None,
                ),
            )
            return cursor.lastrowid

    def listar_nome_empresas(self) -> list[str]:
        with self.base_repository.transaction() as cursor:
            cursor.execute("SELECT nome FROM empresas ORDER BY nome")
            return [row[0].capitalize() for row in cursor.fetchall()]

    def buscar_empresa_por_nome(self, nome: str) -> Optional[Empresa]:
        """Retorna os dados de uma empresa através do nome"""
        if not nome:
            return None

        with self.base_repository.transaction() as cursor:
            cursor.execute(
                """SELECT id, nome, site, setor
                FROM empresas WHERE nome = ?""",
                (nome.lower(),),
            )
            empresa = cursor.fetchone()

        if empresa:
            return Empresa(
                id=empresa[0], nome=empresa[1], site=empresa[2], setor=empresa[3]
            )
        return None

    def buscar_empresa_por_link(self, link: str) -> Optional[Empresa]:
        if not link:
            return None

        with self.base_repository.transaction() as cursor:
            cursor.execute(
                """SELECT id, nome, site, setor
                FROM empresas WHERE site = ?""",
                (link,),
            )
            empresa = cursor.fetchone()

        if empresa:
            return Empresa(
                id=empresa[0], nome=empresa[1], site=empresa[2], setor=empresa[3]
            )
        return None
