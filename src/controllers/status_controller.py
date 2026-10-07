"""
Rota de status da API, usada para conferir se o servidor esta no ar.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Status"])


@router.get("/")
def status_da_api() -> dict:
    return {
        "mensagem": "API Bulbe no ar. Acesse /docs para o Swagger.",
        "versao": "v1",
    }
