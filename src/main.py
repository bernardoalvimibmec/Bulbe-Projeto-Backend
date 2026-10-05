"""
Ponto de entrada da API Bulbe.

Responsabilidades deste arquivo:
- criar o app FastAPI;
- registrar os routers (camada de Apresentacao);
- decidir qual implementacao de repositorio cada servico recebe
  (Sprint 2: em memoria; Sprint 3: SQLAlchemy). E o UNICO lugar que muda
  quando o banco entrar;
- converter todo erro para o formato do contrato
  (docs/api/openapi.yaml, schema Erro): codigo, mensagem, detalhes, request_id.

Rodar localmente:  uvicorn src.main:app --reload
"""

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
# Cada story registra o seu router aqui, por exemplo:
# app.include_router(usina_router)


def _request_id(request: Request) -> str:
    return request.headers.get("X-Request-ID") or f"req_{uuid4().hex[:12]}"


def resposta_de_erro(
    request: Request,
    status: int,
    codigo: str,
    mensagem: str,
    detalhes: list[dict] | None = None,
) -> JSONResponse:
    """Monta o corpo de erro padrao. Todo erro da API sai por aqui."""
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
    # O contrato usa 400 para JSON, campos ou parametros invalidos.
    # 422 fica reservado para regra de negocio (ex.: cliente inelegivel).
    detalhes = [
        {
            # loc vem como ("body", "email"); o primeiro item so diz onde estava o campo
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
