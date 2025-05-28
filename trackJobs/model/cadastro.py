import sqlite3

from trackJobs.banco_de_dados import BancoDeDados
from trackJobs.exceptions import CampoDuplicadoException
from trackJobs.exceptions import ErroCandidaturaException


def get_campos_cadastro_vaga(db: BancoDeDados):
    """Retorna os campos necessários para cadastro de vaga"""
    cursor = db.cursor

    cursor.execute("PRAGMA table_info(vagas)")
    colunas_vagas = [row[1] for row in cursor.fetchall()]

    colunas_vagas.remove("id")
    colunas_vagas.remove("idEmpresa")

    return colunas_vagas


def get_campos_cadastro_empresa(db: BancoDeDados):
    """Retorna os campos necessários para cadastro de empresa"""
    cursor = db.cursor

    cursor.execute("PRAGMA table_info(empresas)")
    colunas_empresas = [row[1] + "_empresa" for row in cursor.fetchall()]

    colunas_empresas.remove("id_empresa")
    return colunas_empresas


def get_empresa_por_nome(db: BancoDeDados, nome_empresa: str):
    """Retorna os dados de uma empresa através do nome"""
    if not nome_empresa:
        return None

    db.cursor.execute(
        "SELECT nome, site, setor FROM empresas WHERE nome = ?", (nome_empresa,)
    )
    empresa = db.cursor.fetchone()

    if empresa:
        return {
            "nome_empresa": empresa[0],
            "site_empresa": empresa[1],
            "setor_empresa": empresa[2],
        }
    return None


def verifica_empresa_por_nome(db: BancoDeDados, nome_empresa: str):
    """Verifica se uma empresa já está cadastrada pelo nome"""
    if not nome_empresa:
        return None

    db.cursor.execute("SELECT id FROM empresas WHERE nome = ?", (nome_empresa,))
    id_empresa = db.cursor.fetchone()

    if id_empresa:
        return id_empresa[0]
    return None


def cadastra_empresa(db: BancoDeDados, dados_empresa: str):
    """Cadastra uma nova empresa no banco de dados"""
    cursor_db = db.cursor

    msg_insert_empresas = """
        INSERT INTO empresas (nome, site, setor) VALUES
        (?, ?, ?)
        """
    cursor_db.execute(
        msg_insert_empresas,
        (
            dados_empresa["nome_empresa"],
            dados_empresa["site_empresa"] if dados_empresa["site_empresa"] else None,
            dados_empresa["setor_empresa"] if dados_empresa["setor_empresa"] else None,
        ),
    )
    db.conexao.commit()


def cadastra_vaga(db: BancoDeDados, dados_candidatura: dict):
    """Cadastra uma nova vaga no banco de dados"""
    cursor_db = db.cursor
    id_empresa = verifica_empresa_por_nome(db, dados_candidatura["nome_empresa"])
    msg_insert_vagas = """INSERT INTO vagas
        (nome, link, status, descriçao, data_aplicaçao, idEmpresa) VALUES
        (?, ?, ?, ?, ?, ?)"""
    params = (
        dados_candidatura["nome"],
        dados_candidatura["link"],
        dados_candidatura["status"],
        dados_candidatura["descriçao"],
        dados_candidatura["data_aplicaçao"],
        id_empresa,
    )

    cursor_db.execute(msg_insert_vagas, params)
    db.conexao.commit()


def cadastra_candidatura(dados_candidatura, db_path="track_jobs.db", teste=False):
    """Cadastra uma nova vaga/empresa no banco de dados"""
    try:
        db = BancoDeDados(db_path)
        empresa_existe = verifica_empresa_por_nome(
            db, dados_candidatura["nome_empresa"]
        )
        if not empresa_existe and dados_candidatura["nome_empresa"]:
            cadastra_empresa(db, dados_candidatura)
        cadastra_vaga(db, dados_candidatura)

    except sqlite3.IntegrityError as e:
        erro_duplicado = str(e)
        campo_duplicado = erro_duplicado.split(" ")[-1]
        db.conexao.rollback()
        raise CampoDuplicadoException(
            f"Erro: O campo '{campo_duplicado}' já está cadastrado."
        )

    except Exception:
        db.conexao.rollback()
        raise ErroCandidaturaException()
