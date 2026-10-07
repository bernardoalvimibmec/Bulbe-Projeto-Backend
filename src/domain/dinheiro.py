"""
Objeto de valor Dinheiro.

O contrato da API representa todo valor monetario como { valor, moeda }.
Aqui essa ideia vira uma classe com regras proprias:
- o valor nunca e negativo e sempre tem 2 casas decimais;
- so se soma dinheiro da mesma moeda (somar reais com dolares e um erro).

Usamos Decimal, e nao float, porque float arredonda errado com dinheiro
(0.1 + 0.2 = 0.30000000000000004).
"""

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
        # frozen=True impede atribuicao direta; object.__setattr__ e o jeito de normalizar no construtor.
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
