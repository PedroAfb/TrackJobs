from typing import Optional

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.model.entities.empresa import Empresa


class SQLiteEmpresaRepository:
    def __init__(self, db: BancoDeDados):
        self.db = db

    def listar_campos_empresa(self) -> list[str]:
        """Retorna os campos necessários para cadastro de empresa"""
        cursor = self.db.cursor

        cursor.execute("PRAGMA table_info(empresas)")
        colunas_empresas = [row[1] + "_empresa" for row in cursor.fetchall()]

        colunas_empresas.remove("id_empresa")
        return colunas_empresas

    def cadastrar_empresa(self, empresa: Empresa) -> None:
        """Cadastra uma nova empresa no banco de dados"""
        cursor_db = self.db.cursor

        msg_insert_empresas = """
            INSERT INTO empresas (nome, site, setor) VALUES
            (?, ?, ?)
            """
        cursor_db.execute(
            msg_insert_empresas,
            (
                empresa.nome,
                empresa.site if empresa.site else None,
                empresa.setor if empresa.setor else None,
            ),
        )
        self.db.conexao.commit()

    def listar_nome_empresas(self) -> list[str]:
        cursor = self.db.cursor
        cursor.execute("SELECT nome FROM empresas ORDER BY nome")
        self.db.conexao.commit()
        return [row[0].capitalize() for row in cursor.fetchall()]

    def buscar_empresa_por_nome(self, nome: str) -> Optional[Empresa]:
        """Retorna os dados de uma empresa através do nome"""
        if not nome:
            return None

        self.db.cursor.execute(
            "SELECT nome, site, setor FROM empresas WHERE nome = ?", (nome,)
        )
        empresa = self.db.cursor.fetchone()

        if empresa:
            return Empresa(nome=empresa[0], site=empresa[1], setor=empresa[2])
        return None
