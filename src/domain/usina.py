"""
Entidade Usina (US06 — listar usinas ativas).

Segue o diagrama de classes (docs/diagramas/classes-dominio.puml):
id, nome, cidade, estado, regiao, status, atualizadaEm.

Regras que moram na propria usina:
- os dados basicos sao validados na criacao (nome, UF com 2 letras, status conhecido);
- a usina sabe dizer se esta ativa;
- a usina sabe se deve aparecer numa listagem: sem filtro, so as ativas
  aparecem para o publico; com filtro, so as do status pedido.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.domain.erros import DadoInvalido


class StatusUsina(str, Enum):
    ativa = "ativa"
    em_manutencao = "em_manutencao"
    inativa = "inativa"


@dataclass
class Usina:
    id: str
    nome: str
    cidade: str
    estado: str
    regiao: str
    status: StatusUsina
    atualizada_em: datetime

    def __post_init__(self) -> None:
        if len(self.nome.strip()) < 3:
            raise DadoInvalido("nome", "O nome da usina deve ter pelo menos 3 caracteres.")
        estado = self.estado.strip().upper()
        if len(estado) != 2 or not estado.isalpha():
            raise DadoInvalido("estado", "O estado deve ser a sigla da UF, por exemplo MG.")
        self.estado = estado
        try:
            self.status = StatusUsina(self.status)
        except ValueError:
            raise DadoInvalido(
                "status", "Status deve ser ativa, em_manutencao ou inativa."
            ) from None

    def esta_ativa(self) -> bool:
        return self.status == StatusUsina.ativa

    def aparece_na_listagem(self, status_filtro: StatusUsina | None = None) -> bool:
        """Regra da US06: sem filtro, o publico ve so as usinas ativas."""
        if status_filtro is None:
            return self.esta_ativa()
        return self.status == StatusUsina(status_filtro)

    @property
    def localizacao(self) -> str:
        return f"{self.cidade} - {self.estado}"
