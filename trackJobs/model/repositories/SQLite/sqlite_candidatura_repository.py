from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.model.entities.candidatura import Candidatura


class SQLiteCandidaturaRepository:
    def __init__(self, db: BancoDeDados):
        self.db = db

    def cadastrar_candidatura(self, candidatura: Candidatura):
        """Cadastra uma nova candidatura no banco de dados"""
        cursor = self.db.cursor

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
        self.db.conexao.commit()
