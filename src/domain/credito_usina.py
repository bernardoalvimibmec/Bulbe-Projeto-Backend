"""Creditos por usina (US07) e resumo de creditos (US08)."""

from dataclasses import dataclass
from datetime import datetime

from src.domain.competencia import Competencia
from src.domain.dinheiro import Dinheiro
from src.domain.erros import FonteIndisponivel
from src.domain.usina import StatusUsina, Usina

_NOME_DO_CRITERIO = {
    StatusUsina.ativa: "usinas_ativas",
    StatusUsina.em_manutencao: "usinas_em_manutencao",
    StatusUsina.inativa: "usinas_inativas",
}


@dataclass(frozen=True)
class CreditoUsina:
    usina_id: str
    competencia: Competencia
    creditos: Dinheiro
    atualizado_em: datetime

    def pertence_a(self, usina_id: str, competencia: Competencia) -> bool:
        return self.usina_id == usina_id and self.competencia == competencia

    def obter_valor(self) -> Dinheiro:
        return self.creditos


@dataclass(frozen=True)
class ResumoCreditos:
    competencia: Competencia
    criterio: str
    quantidade_usinas: int
    total_creditos: Dinheiro
    atualizado_em: datetime | None

    @classmethod
    def calcular(
        cls,
        competencia: Competencia,
        usinas: list[Usina],
        creditos: list[CreditoUsina],
        status_usina: StatusUsina = StatusUsina.ativa,
        moeda: str = "BRL",
    ) -> "ResumoCreditos":
        usinas_do_criterio = [u for u in usinas if u.status == StatusUsina(status_usina)]

        creditos_usados: list[CreditoUsina] = []
        sem_credito: list[str] = []
        for usina in usinas_do_criterio:
            credito = next((c for c in creditos if c.pertence_a(usina.id, competencia)), None)
            if credito is None:
                sem_credito.append(usina.id)
            else:
                creditos_usados.append(credito)

        if sem_credito:
            raise FonteIndisponivel(
                f"Os creditos de {len(sem_credito)} usina(s) ainda nao foram informados "
                f"para {competencia}. O total nao e exibido incompleto."
            )

        total = Dinheiro.zero(moeda)
        for credito in creditos_usados:
            total = total + credito.creditos

        atualizado_em = min((c.atualizado_em for c in creditos_usados), default=None)

        return cls(
            competencia=competencia,
            criterio=_NOME_DO_CRITERIO[StatusUsina(status_usina)],
            quantidade_usinas=len(usinas_do_criterio),
            total_creditos=total,
            atualizado_em=atualizado_em,
        )
