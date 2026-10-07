"""Testes das regras de Depoimento (US11)."""

from decimal import Decimal

import pytest

from src.domain.depoimento import Depoimento
from src.domain.dinheiro import Dinheiro
from src.domain.erros import DadoInvalido, RecursoNaoEncontrado


def novo_depoimento(**mudancas):
    dados = dict(
        id="depoimento_01",
        nome_publico="Cliente de Minas Gerais",
        localidade="Montes Claros - MG",
        avaliacao=5,
        texto="Minha experiencia foi positiva.",
        publicacao_autorizada=True,
        economia_mensal=Dinheiro(Decimal("85.40")),
        dias_para_ativacao=72,
        percentual_desconto=15,
        tempo_conta_ativa_meses=8,
        cliente_id="cliente_01",
    )
    dados.update(mudancas)
    return Depoimento(**dados)


def test_autorizado_pode_ser_publicado():
    assert novo_depoimento().pode_ser_publicado() is True


def test_sem_autorizacao_nao_pode_ser_publicado():
    assert novo_depoimento(publicacao_autorizada=False).pode_ser_publicado() is False


def test_sem_texto_nao_pode_ser_publicado():
    assert novo_depoimento(texto="   ").pode_ser_publicado() is False


def test_dados_publicos_nao_expoem_o_cliente():
    publicos = novo_depoimento().dados_publicos()
    assert "cliente_id" not in publicos
    assert "publicacao_autorizada" not in publicos
    assert publicos["economia_mensal"] == {"valor": 85.40, "moeda": "BRL"}


def test_nao_autorizado_responde_como_nao_encontrado():
    with pytest.raises(RecursoNaoEncontrado) as erro:
        novo_depoimento(publicacao_autorizada=False).dados_publicos()
    assert erro.value.status == 404


@pytest.mark.parametrize(
    "campo, valor",
    [("avaliacao", 0), ("avaliacao", 6), ("percentual_desconto", 120), ("dias_para_ativacao", -1)],
)
def test_valores_fora_da_regra_sao_recusados(campo, valor):
    with pytest.raises(DadoInvalido):
        novo_depoimento(**{campo: valor})
