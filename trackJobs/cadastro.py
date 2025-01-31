import validators
from rich.prompt import Prompt
from rich.console import Console
import click
import sqlite3
from sqlite3 import Connection, Cursor

console = Console()
VOLTAR_MENU = 6


def obter_site_empresa(cursor: Cursor):
    while True:
        site_empresa = Prompt.ask("Qual o site da empresa?[OPCIONAL]")

        if not site_empresa:
            return None
        elif validators.url(site_empresa):
            cursor.execute("SELECT 1 FROM empresas WHERE site = ?", (site_empresa,))
            if cursor.fetchone():
                raise sqlite3.IntegrityError("empresas.site")
            return site_empresa
        else:
            print("[bold red]URL inválida. Digite um link válido ou deixe em branco.[/bold red]")


def verifica_empresa_sql(cursor: Cursor, nome_empresa: str):
    cursor.execute("SELECT 1 FROM empresas WHERE nome = ?", (nome_empresa,))
    return cursor.fetchone()


def coleta_dados_vaga():
    dados_candidatura = dict()

    nome = click.prompt(
        "Qual o nome da vaga?[OBRIGATÓRIO]\n"
        "Caso queira retornar ao menu, digite 6")
    if int(nome) == VOLTAR_MENU:
        return
    dados_candidatura["nome"] = nome.strip().lower()

    dados_candidatura["link"] = click.prompt("Qual o link da vaga?[OBRIGATÓRIO]") # tem que ser unique
    dados_candidatura["status"] = Prompt.ask(
        "Qual o status da candidatura?[OPCIONAL]",
        choices=["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"],
        default="candidatar-se",
        show_default=False)
    dados_candidatura["descricao"] = Prompt.ask("Coloque descrição sobre a vaga[OPCIONAL]")
    nome_empresa = Prompt.ask("Qual o nome da empresa?[OPCIONAL]")
    dados_candidatura["nome_empresa"] = nome_empresa.strip().lower()

    return dados_candidatura


def cadastra_empresa(conexao: Connection, cursor: Cursor, nome_empresa: str):
    site_empresa = obter_site_empresa(cursor)
    setor_empresa = Prompt.ask("Qual o setor da empresa?[OPCIONAL]")

    msg_insert_empresas = (f"""
        INSERT INTO empresas (nome, site, setor) VALUES
        ('{nome_empresa}', '{site_empresa}', '{setor_empresa}')
        """)
    cursor.execute(msg_insert_empresas)
    conexao.commit()


def cadastra_vaga(conexao: Connection, cursor: Cursor, dados_candidatura: dict):
    if dados_candidatura["nome_empresa"]:    # Adiciona vaga com uma empresa associada
        id_empresa = cursor.execute("SELECT id FROM empresas WHERE nome = ?", (dados_candidatura["nome_empresa"],)).fetchall()[0][0]
        msg_insert_vagas = (
            "INSERT INTO vagas (nome, link, status, descricao, idEmpresa) VALUES\n"
            f"('{dados_candidatura['nome']}', '{dados_candidatura['link']}', '{dados_candidatura['status']}', '{dados_candidatura['descricao']}', '{id_empresa}')"
        )
    else:
        msg_insert_vagas = (
        "INSERT INTO vagas (nome, link, status, descricao) VALUES\n"
        f"('{dados_candidatura['nome']}', '{dados_candidatura['link']}', '{dados_candidatura['status']}', '{dados_candidatura['descricao']}')"
        )

    cursor.execute(msg_insert_vagas)
    conexao.commit()


def cadastra_candidatura():
    console.print("[bold magenta]\nCadastro[/bold magenta]\n")

    dados_candidatura = coleta_dados_vaga()

    try:
        conexao = sqlite3.connect("track_jobs.db")
        cursor = conexao.cursor()

        nome_empresa = dados_candidatura["nome_empresa"]
        empresa_existe = verifica_empresa_sql(cursor, nome_empresa)
        

        if nome_empresa and not empresa_existe:    # Se o usuário escreveu no campo empresa e ela não está no banco de dados, o cadastro da empresa é realizado
            cadastra_empresa(conexao, cursor, nome_empresa)

        cadastra_vaga(conexao, cursor, dados_candidatura)
        
        console.print("[bold green]\nCadastro realizado com sucesso!\n[/bold green]")
        conexao.close()

    except sqlite3.IntegrityError as e:
        conexao.close()
        erro_duplicado = str(e)
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {erro_duplicado}")
        campo_duplicado = erro_duplicado.split(" ")[-1]
        console.print(
            f"[bold red]Erro ao cadastrar no banco de dados: {campo_duplicado} já foi cadastrada![/bold red]"
        )
        cadastra_candidatura()

    except Exception as e:
        conexao.close()
        console.print("[bold red]Erro inesperado ao cadastrar a vaga.[/bold red]")
        console.print(f"[bold yellow]Detalhes:[/bold yellow] {str(e)}")
        cadastra_candidatura()