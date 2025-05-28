from trackJobs.exceptions import TrackJobsException
from trackJobs.model.job_model import JobModel


class JobController:
    job_model: JobModel

    def __init__(self, job_model: JobModel):
        self.job_model = job_model

    def campos_perguntas_vaga(self):
        perguntas_padrao = {
            "nome": "Qual o nome da vaga?[OBRIGATÓRIO]\n",
            "link": "Qual o link da vaga?[OBRIGATÓRIO]\n",
            "status": "Qual o status da vaga?\n",
            "data_aplicaçao": "Qual a data da candidatura (YYYY-MM-DD)?[OPCIONAL]\n",
            "descriçao": "Coloque descrição sobre a vaga[OPCIONAL]\n",
        }

        colunas_vagas = self.job_model.campos_cadastro_vaga()
        campos_vagas = {}
        for coluna in colunas_vagas:
            campos_vagas[coluna] = perguntas_padrao.get(
                coluna, f"Informe o valor para {coluna}:\n"
            )

        return campos_vagas

    def campos_perguntas_empresa(self):
        colunas_empresas = self.job_model.campos_cadastro_empresa()
        perguntas_padrao = {
            "nome_empresa": "Qual o nome da empresa?[OBRIGATÓRIO]\n",
            "site_empresa": "Qual o site da empresa?[OPCIONAL]\n",
            "setor_empresa": "Qual o setor da empresa?[OPCIONAL]\n",
        }

        campos_empresas = {}
        for coluna in colunas_empresas:
            campos_empresas[coluna] = perguntas_padrao.get(
                coluna, f"Informe o valor para {coluna}:\n"
            )

        return campos_empresas

    def validar_campo(self, campo, valor, console):
        try:
            return self.job_model.validar_campo(campo, valor, console)
        except TrackJobsException as e:
            return f"[bold red]{e.args[0]}[/bold red]"

    def obter_opcoes_empresa(self):
        """Retorna as opções disponíveis para empresa"""
        empresas_existentes = self.job_model.listar_nome_empresas()
        opcoes = ["Não atrelar empresa", "Cadastrar nova empresa"]

        if empresas_existentes:
            opcoes.extend(empresas_existentes)

        return opcoes

    def processar_escolha_empresa(self, escolha):
        """Processa a escolha do usuário sobre empresa"""
        if escolha == "Não atrelar empresa":
            return {"tipo": "nenhuma", "dados": None}
        elif escolha == "Cadastrar nova empresa":
            return {"tipo": "nova", "dados": None}
        else:
            return {"tipo": "existente", "dados": escolha}

    def obter_dados_empresa(self, nome_empresa):
        """Obtém os dados da empresa pelo nome"""
        return self.job_model.get_empresa(nome_empresa)

    def cadastra_candidatura(self, dados_candidatura):
        try:
            self.job_model.cadastro(dados_candidatura)
            return (
                "[bold green]\nCadastro da vaga realizado com sucesso!\n[/bold green]"
            )
        except TrackJobsException as e:
            raise e
