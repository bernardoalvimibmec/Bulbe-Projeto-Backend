"""
Erros de negocio do dominio.

Os servicos levantam essas excecoes; quem transforma em resposta HTTP e o
handler registrado em src/main.py. Assim nenhum servico precisa saber de HTTP.
"""


class ErroDeNegocio(Exception):
    """Erro de negocio no formato do contrato: codigo, mensagem e status HTTP."""

    def __init__(
        self,
        codigo: str,
        mensagem: str,
        status: int,
        detalhes: list[dict] | None = None,
    ) -> None:
        self.codigo = codigo
        self.mensagem = mensagem
        self.status = status
        self.detalhes = detalhes or []
        super().__init__(mensagem)


class DadoInvalido(ErroDeNegocio):
    """Um valor que o dominio recusa (ex.: competencia fora do formato AAAA-MM). Vira 400."""

    def __init__(self, campo: str, mensagem: str) -> None:
        super().__init__(
            "REQUISICAO_INVALIDA",
            mensagem,
            400,
            detalhes=[{"campo": campo, "mensagem": mensagem}],
        )


class RecursoNaoEncontrado(ErroDeNegocio):
    def __init__(self, mensagem: str = "O recurso solicitado nao foi encontrado.") -> None:
        super().__init__("RECURSO_NAO_ENCONTRADO", mensagem, 404)


class NaoAutenticado(ErroDeNegocio):
    def __init__(self, mensagem: str = "E necessario estar autenticado.") -> None:
        super().__init__("NAO_AUTENTICADO", mensagem, 401)


class AcessoNegado(ErroDeNegocio):
    def __init__(self, mensagem: str = "Voce nao tem permissao para acessar este recurso.") -> None:
        super().__init__("ACESSO_NEGADO", mensagem, 403)


class FonteIndisponivel(ErroDeNegocio):
    def __init__(
        self,
        mensagem: str = "Os dados nao estao disponiveis no momento. Tente novamente mais tarde.",
    ) -> None:
        super().__init__("FONTE_INDISPONIVEL", mensagem, 503)
