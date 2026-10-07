"""Objeto de valor Competencia (AAAA-MM)."""

import re
from dataclasses import dataclass

from src.domain.erros import DadoInvalido

_FORMATO = re.compile(r"^(\d{4})-(\d{2})$")


@dataclass(frozen=True, order=True)
class Competencia:
    ano: int
    mes: int

    def __post_init__(self) -> None:
        if not 1 <= self.mes <= 12:
            raise DadoInvalido("competencia", "O mes da competencia deve estar entre 01 e 12.")
        if not 2000 <= self.ano <= 2100:
            raise DadoInvalido("competencia", "Ano da competencia fora do intervalo aceito.")

    @classmethod
    def de_texto(cls, texto: str) -> "Competencia":
        encontrado = _FORMATO.match(texto or "")
        if not encontrado:
            raise DadoInvalido("competencia", "Use o formato AAAA-MM, por exemplo 2026-08.")
        return cls(int(encontrado.group(1)), int(encontrado.group(2)))

    def __str__(self) -> str:
        return f"{self.ano:04d}-{self.mes:02d}"
