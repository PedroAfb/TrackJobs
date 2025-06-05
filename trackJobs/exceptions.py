class TrackJobsException(Exception):
    def __init__(self, message="Erro desconhecido no TrackJobs."):
        super().__init__(message)


class InicializacaoBancoException(TrackJobsException):
    def __init__(self, message="Erro ao inicializar o banco de dados."):
        super().__init__(message)


class RetornarMenuException(TrackJobsException):
    def __init__(self, message="Retornando ao menu principal."):
        super().__init__(message)


class URLJaCadastradaException(TrackJobsException):
    def __init__(self, message="Erro: URL já cadastrada."):
        super().__init__(message)


class URLNaoInformadaException(TrackJobsException):
    def __init__(self, message="Erro: URL não informada."):
        super().__init__(message)


class NomeVazioException(TrackJobsException):
    def __init__(self, message="Erro: O nome não pode ser vazio."):
        super().__init__(message)


class URLInvalidaException(TrackJobsException):
    def __init__(self, message="Erro: Formato da URL inválida."):
        super().__init__(message)


class DataInvalidaException(TrackJobsException):
    def __init__(self, message="Erro: Formato da Data é inválido."):
        super().__init__(message)


class StatusInvalidoException(TrackJobsException):
    def __init__(
        self,
        message="Erro: Status deve ter os seguintes valores: "
        "candidatar-se, em análise, entrevista, rejeitado, aceito.",
    ):
        super().__init__(message)


class ErroCandidaturaException(TrackJobsException):
    def __init__(self, message="Erro: ao realizar candidatura."):
        super().__init__(message)


class CampoDuplicadoException(TrackJobsException):
    def __init__(self, message="Erro: Esse Campo já foi cadastrado."):
        super().__init__(message)


class CampoInvalidoException(TrackJobsException):
    def __init__(self, message="Erro: Campo inválido."):
        super().__init__(message)
