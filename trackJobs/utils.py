import sqlite3

import questionary
from questionary import Style

OPCOES_STATUS = ["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"]
CUSTOM_STYLE = Style(
    [
        ("qmark", "fg:#00ffff bold"),  # Sinal de pergunta (ex: ?)
        ("question", "bold"),  # Pergunta principal
        ("answer", "fg:#00ffff bold"),  # Resposta selecionada
        (
            "pointer",
            "fg:#00ffff bold",
        ),  # Seta que aponta para a opção selecionada
        (
            "highlighted",
            "fg:#00ffff bold",
        ),  # Opção em destaque (mouse ou seleção)
        ("selected", "fg:#00ffff"),  # Quando uma opção já está selecionada
        ("separator", "fg:#6C6C6C"),  # Separador de opções, se usado
        ("instruction", ""),  # Instruções adicionais (ex: Pressione enter)
    ]
)


def realiza_update(db_path, candidatura, campo, novo_dado):
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()

    comando = (
        f"UPDATE vagas SET '{campo}' = ? WHERE link = ?"  # Configura SQL Injection?
    )
    cursor.execute(comando, (novo_dado, candidatura["link"]))
    conexao.commit()
    conexao.close()


def get_vaga(db_path, link):
    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()

    comando = "SELECT * FROM vagas WHERE link = ?"
    cursor.execute(comando, (link,))
    vaga = cursor.fetchone()

    conexao.close()
    if vaga:
        # Pega o nome das colunas
        colunas = [descricao[0] for descricao in cursor.description]

        # Cria um dicionário combinando as colunas com os valores
        vaga_dict = dict(zip(colunas, vaga))

        return vaga_dict
    else:
        return None  # Caso não encontre a vaga


def get_candidaturas_com_filtro(db_path, filtro="", tipo_filtro=None):
    conexao = sqlite3.connect(db_path)
    conexao.row_factory = sqlite3.Row  # Retorna os resultados como dicionário
    cursor = conexao.cursor()
    query = "SELECT nome, link, status FROM vagas"
    params = []

    if tipo_filtro in ["link", "nome", "status"]:
        query += f" WHERE {tipo_filtro} LIKE ?"
        params.append(f"%{filtro}%")

    cursor.execute(query, params)
    candidaturas = [dict(row) for row in cursor.fetchall()]
    conexao.close()
    return candidaturas


def filtra_candidaturas(db_path, index_candidatura):
    """
    Filtra as candidaturas com base na opção selecionada.
    """
    if index_candidatura == "link":
        filtro_link = questionary.text(
            "\nDigite o link da candidatura para filtrar:\n"
        ).ask()
        return get_candidaturas_com_filtro(
            db_path, filtro=filtro_link, tipo_filtro="link"
        )

    elif index_candidatura == "nome":
        filtro_nome = questionary.text(
            "\nDigite o nome da candidatura para filtrar:\n"
        ).ask()
        return get_candidaturas_com_filtro(
            db_path, filtro=filtro_nome, tipo_filtro="nome"
        )

    elif index_candidatura == "status":
        filtro_status = questionary.select(
            "\nSelecione o status da candidatura para filtrar:\n",
            choices=OPCOES_STATUS,
        ).ask()
        return get_candidaturas_com_filtro(
            db_path, filtro=filtro_status, tipo_filtro="status"
        )

    return get_candidaturas_com_filtro(db_path)
