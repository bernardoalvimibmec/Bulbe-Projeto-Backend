"""Rota de status da API."""

from fastapi import APIRouter

router = APIRouter(tags=["Status"])


@router.get("/")
def status_da_api() -> dict:
    return {
        "mensagem": "API Bulbe no ar. Acesse /docs para o Swagger.",
        "versao": "v1",
    }
