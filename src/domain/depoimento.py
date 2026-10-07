"""Entidade Depoimento (US11)."""

from dataclasses import dataclass
from decimal import Decimal

from src.domain.dinheiro import Dinheiro
from src.domain.erros import DadoInvalido, RecursoNaoEncontrado


@dataclass
class Depoimento:
    id: str
    nome_publico: str
    localidade: str
    avaliacao: int
    texto: str
    publicacao_autorizada: bool
    economia_mensal: Dinheiro | None = None
    dias_para_ativacao: int | None = None
    percentual_desconto: Decimal | None = None
    tempo_conta_ativa_meses: int | None = None
    cliente_id: str | None = None

    def __post_init__(self) -> None:
        if not 1 <= self.avaliacao <= 5:
            raise DadoInvalido("avaliacao", "A avaliacao deve ser de 1 a 5.")
        if self.dias_para_ativacao is not None and self.dias_para_ativacao < 0:
            raise DadoInvalido("dias_para_ativacao", "Dias para ativacao nao pode ser negativo.")
        if self.tempo_conta_ativa_meses is not None and self.tempo_conta_ativa_meses < 0:
            raise DadoInvalido("tempo_conta_ativa_meses", "Tempo de conta ativa nao pode ser negativo.")
        if self.percentual_desconto is not None:
            self.percentual_desconto = Decimal(str(self.percentual_desconto))
            if not Decimal("0") <= self.percentual_desconto <= Decimal("100"):
                raise DadoInvalido("percentual_desconto", "O desconto deve estar entre 0 e 100%.")

    def pode_ser_publicado(self) -> bool:
        return self.publicacao_autorizada and bool(self.texto.strip())

    def dados_publicos(self) -> dict:
        if not self.pode_ser_publicado():
            raise RecursoNaoEncontrado("Depoimento nao encontrado.")
        return {
            "id": self.id,
            "nome_publico": self.nome_publico,
            "localidade": self.localidade,
            "avaliacao": self.avaliacao,
            "economia_mensal": (
                {"valor": float(self.economia_mensal.valor), "moeda": self.economia_mensal.moeda}
                if self.economia_mensal
                else None
            ),
            "dias_para_ativacao": self.dias_para_ativacao,
            "percentual_desconto": (
                float(self.percentual_desconto) if self.percentual_desconto is not None else None
            ),
            "tempo_conta_ativa_meses": self.tempo_conta_ativa_meses,
            "texto": self.texto,
        }
