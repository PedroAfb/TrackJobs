import questionary

from trackJobs.controller.job_controller import JobController
from trackJobs.exceptions import RetornarMenuException
from trackJobs.exceptions import TrackJobsException
from trackJobs.view.menus.menu_edicao import MenuEdicao


class EdicaoCliView:
    def __init__(self, tela, controller: JobController):
        self.tela = tela
        self.controller = controller
        self.menu_edicao = MenuEdicao(tela, controller=controller)

    def edicao(self):
        try:
            cand_selecionada = self.menu_edicao.escolha_candidatura()
            campo_selecionado = self.menu_edicao.menu_edicao(cand_selecionada)
            self.tela.clear()
            validacao = False

            while validacao is not True:
                self.tela.clear()
                novo_dado = (
                    questionary.text(
                        "\nInforme o novo valor do campo "
                        f"{campo_selecionado.capitalize()}:\n",
                    )
                    .ask()
                    .strip()
                )
                validacao = self.controller.validar_campo(campo_selecionado, novo_dado)
                if isinstance(validacao, str):
                    self.tela.clear()
                    self.tela.addstr(5, 5, validacao)
                    self.tela.refresh()

            self.controller.atualizar_candidatura(
                cand_selecionada, campo_selecionado, novo_dado
            )
            self.menu_edicao.exibe_mensagem_sucesso(
                None, campo_selecionado.capitalize()
            )
        except RetornarMenuException:
            pass

        except TrackJobsException as e:
            self.menu_edicao.exibe_mensagem_erro(str(e))
