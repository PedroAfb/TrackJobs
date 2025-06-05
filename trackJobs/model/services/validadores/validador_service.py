from .empresa_validador_service import EmpresaValidadorService
from .vaga_validador_service import VagaValidadorService


class ValidadorService:
    def __init__(
        self,
        empresa_validador: EmpresaValidadorService,
        vaga_validador: VagaValidadorService,
    ):
        self.empresa_validador = empresa_validador
        self.vaga_validador = vaga_validador
        self.VALIDADORES = {
            "nome": lambda nome: self.vaga_validador.valida_nome(nome),
            "link": lambda link: self.vaga_validador.valida_link(link),
            "status": lambda status: self.vaga_validador.valida_status(status),
            "descriçao": lambda descricao: True,
            "data_aplicaçao": lambda data: self.vaga_validador.valida_data_aplicacao(
                data
            ),
            "nome_empresa": lambda nome_empresa: (
                self.empresa_validador.valida_nome_empresa(nome_empresa)
            ),
            "site_empresa": lambda site_empresa: (
                self.empresa_validador.valida_link_empresa(site_empresa)
            ),
            "setor_empresa": lambda setor_empresa: True,
        }
