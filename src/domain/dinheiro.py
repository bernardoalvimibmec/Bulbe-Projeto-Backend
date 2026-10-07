"""Objeto de valor Dinheiro."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from src.domain.erros import DadoInvalido

DUAS_CASAS = Decimal("0.01")


@dataclass(frozen=True)
class Dinheiro:
    valor: Decimal
    moeda: str = "BRL"

    def __post_init__(self) -> None:
        valor = Decimal(str(self.valor)).quantize(DUAS_CASAS, rounding=ROUND_HALF_UP)
        if valor < 0:
            raise DadoInvalido("valor", "Valor monetario nao pode ser negativo.")
        moeda = self.moeda.upper()
        if len(moeda) != 3 or not moeda.isalpha():
            raise DadoInvalido("moeda", "Moeda deve seguir o padrao ISO 4217, por exemplo BRL.")
        object.__setattr__(self, "valor", valor)
        object.__setattr__(self, "moeda", moeda)

    @classmethod
    def zero(cls, moeda: str = "BRL") -> "Dinheiro":
        return cls(Decimal("0"), moeda)

    def somar(self, outro: "Dinheiro") -> "Dinheiro":
        if self.moeda != outro.moeda:
            raise DadoInvalido(
                "moeda",
                f"Nao e possivel somar {self.moeda} com {outro.moeda}.",
            )
        return Dinheiro(self.valor + outro.valor, self.moeda)

    def __add__(self, outro: "Dinheiro") -> "Dinheiro":
        return self.somar(outro)
