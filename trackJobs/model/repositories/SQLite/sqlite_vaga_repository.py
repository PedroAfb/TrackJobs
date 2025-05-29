from trackJobs.banco_de_dados import BancoDeDados


class SQLiteVagaRepository:
    def __init__(self, db: BancoDeDados):
        self.db = db

    def listar_campos_vaga(self) -> list[str]:
        """Retorna os campos necessários para cadastro de vaga"""
        cursor = self.db.cursor

        cursor.execute("PRAGMA table_info(vagas)")
        colunas_vagas = [row[1] for row in cursor.fetchall()]

        colunas_vagas.remove("id")
        colunas_vagas.remove("idEmpresa")

        return colunas_vagas
