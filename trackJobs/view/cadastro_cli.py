import questionary

from trackJobs.exceptions import RetornarMenuException
from trackJobs.exceptions import TrackJobsException

BOTAO_RETORNAR_MENU = "6"


class CadastroCliView:
    def __init__(self, controller):
        self.controller = controller

    def cadastro(self) -> None:
        """Método para cadastrar uma nova candidatura"""
        self.console.print("[bold magenta]\nCadastro[/bold magenta]\n")
        try:
            dados_candidatura = self._coletar_dados_vaga()
            escolha_empresa = self._processar_empresa()
        except RetornarMenuException:
            self.console.print(
                "[bold yellow]Retornando ao menu principal...[/bold yellow]"
            )
            return

        dados_candidatura.update(escolha_empresa)

        try:
            mensagem = self.controller.cadastra_candidatura(dados_candidatura)
            self.console.print(mensagem)
        except TrackJobsException as e:
            self.console.print(f"[bold red]{e}[/bold red]")
            return

    def _formatar_campo(self, campo, valor):
        """Formata campos conforme tipo"""
        if not valor:
            return valor

        # Campos que NÃO devem ser convertidos para lowercase
        campos_sem_lower = {
            "link",
            "site_empresa",
            "status",
            "data_aplicacao",
            "descriçao",
        }

        # Sempre fazer strip
        valor_formatado = valor.strip()

        # Aplicar lowercase apenas se necessário
        if campo not in campos_sem_lower:
            valor_formatado = valor_formatado.lower()

        return valor_formatado

    def _coletar_dados_vaga(self):
        """Coleta dados da vaga"""
        campos_vaga = self.controller.campos_perguntas_vaga()
        dados_candidatura = {}
        validacao = False

        for campo, pergunta in campos_vaga.items():
            while validacao is not True:
                if campo == "status":
                    resposta = questionary.select(
                        pergunta,
                        choices=[
                            "candidatar-se",
                            "em análise",
                            "entrevista",
                            "rejeitado",
                            "aceito",
                        ],
                    ).ask()
                else:
                    resposta = questionary.text(
                        pergunta, instruction="Caso queira retornar ao menu, digite 6:"
                    ).ask()

                if resposta == BOTAO_RETORNAR_MENU:
                    raise RetornarMenuException()

                resposta_formatada = self._formatar_campo(campo, resposta)
                validacao = self.controller.validar_campo(campo, resposta_formatada)
                if type(validacao) is str:
                    self.console.print(validacao)

            dados_candidatura[campo] = resposta_formatada
            validacao = False

        return dados_candidatura

    def _processar_empresa(self):
        """Processa a escolha sobre empresa"""
        opcoes_empresa = self.controller.obter_opcoes_empresa()

        escolha = questionary.select(
            "Escolha uma opção para empresa:", choices=opcoes_empresa
        ).ask()

        resultado_escolha = self.controller.processar_escolha_empresa(escolha)

        if resultado_escolha["tipo"] == "nenhuma":
            return {
                "nome_empresa": None,
                "site_empresa": None,
                "setor_empresa": None,
            }

        elif resultado_escolha["tipo"] == "existente":
            return self.controller.obter_dados_empresa(resultado_escolha["dados"])

        elif resultado_escolha["tipo"] == "nova":
            return self._coletar_dados_empresa()

    def _coletar_dados_empresa(self):
        """Coleta dados para nova empresa"""
        campos_empresa = self.controller.campos_perguntas_empresa()
        dados_empresa = {}
        validacao = False

        for campo, pergunta in campos_empresa.items():
            while validacao is not True:
                resposta = questionary.text(
                    pergunta, instruction="Caso queira retornar ao menu, digite 6"
                ).ask()

                if resposta == BOTAO_RETORNAR_MENU:
                    raise RetornarMenuException()

                resposta_formatada = self._formatar_campo(campo, resposta)
                validacao = self.controller.validar_campo(campo, resposta_formatada)
                if type(validacao) is str:
                    self.console.print(validacao)

            dados_empresa[campo] = resposta_formatada
            validacao = False

        return dados_empresa
