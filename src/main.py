"""Ponto de entrada da API Bulbe."""

from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.controllers.status_controller import router as status_router
from src.domain.erros import ErroDeNegocio

app = FastAPI(
    title="API Bulbe Energia",
    description="Backend da plataforma Bulbe Energia, Projeto Ciencia de Dados II (Squad Master).",
    version="1.0.0",
)

app.include_router(status_router)


def _request_id(request: Request) -> str:
    return request.headers.get("X-Request-ID") or f"req_{uuid4().hex[:12]}"


def resposta_de_erro(
    request: Request,
    status: int,
    codigo: str,
    mensagem: str,
    detalhes: list[dict] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            "codigo": codigo,
            "mensagem": mensagem,
            "detalhes": detalhes or [],
            "request_id": _request_id(request),
        },
    )


@app.exception_handler(ErroDeNegocio)
def tratar_erro_de_negocio(request: Request, exc: ErroDeNegocio) -> JSONResponse:
    return resposta_de_erro(request, exc.status, exc.codigo, exc.mensagem, exc.detalhes)


@app.exception_handler(RequestValidationError)
def tratar_erro_de_validacao(request: Request, exc: RequestValidationError) -> JSONResponse:
    detalhes = [
        {
            "campo": ".".join(str(parte) for parte in erro.get("loc", ())[1:]) or str(erro.get("loc", "")),
            "mensagem": erro.get("msg", ""),
        }
        for erro in exc.errors()
    ]
    return resposta_de_erro(
        request,
        400,
        "REQUISICAO_INVALIDA",
        "Um ou mais campos da requisicao sao invalidos.",
        detalhes,
    )


@app.exception_handler(StarletteHTTPException)
def tratar_erro_http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    padroes = {
        401: ("NAO_AUTENTICADO", "E necessario estar autenticado."),
        403: ("ACESSO_NEGADO", "Voce nao tem permissao para acessar este recurso."),
        404: ("RECURSO_NAO_ENCONTRADO", "O recurso solicitado nao foi encontrado."),
        405: ("METODO_NAO_PERMITIDO", "Metodo HTTP nao permitido para esta rota."),
    }
    codigo, mensagem = padroes.get(exc.status_code, ("ERRO_HTTP", str(exc.detail)))
    return resposta_de_erro(request, exc.status_code, codigo, mensagem)
