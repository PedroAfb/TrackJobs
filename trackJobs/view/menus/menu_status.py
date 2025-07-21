import questionary

from trackJobs.controller.job_controller import JobController
from trackJobs.view.menus.menu import Menu

OPCOES_STATUS = ["candidatar-se", "em análise", "entrevista", "rejeitado", "aceito"]


class MenuStatus(Menu):
    def __init__(self, tela, controller: JobController):
        super().__init__(tela, controller=controller)

    def menu_status(self, candidatura):
        novo_status = questionary.select(
            f"\n\n\nEditar status da candidatura {candidatura['nome']} para:",
            choices=OPCOES_STATUS,
        ).ask()

        return novo_status
