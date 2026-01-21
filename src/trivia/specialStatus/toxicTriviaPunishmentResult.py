import locale
from dataclasses import dataclass

from .toxicTriviaPunishment import ToxicTriviaPunishment


@dataclass(frozen = True, slots = True)
class ToxicTriviaPunishmentResult:
    totalPointsStolen: int
    toxicTriviaPunishments: list[ToxicTriviaPunishment]

    @property
    def numberOfToxicTriviaPunishments(self) -> int:
        return len(self.toxicTriviaPunishments)

    @property
    def totalPointsStolenStr(self) -> str:
        return locale.format_string("%d", self.totalPointsStolen, grouping = True)
