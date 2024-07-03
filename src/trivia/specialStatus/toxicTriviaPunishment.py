import locale
from dataclasses import dataclass

from ...cuteness.cutenessResult import CutenessResult


@dataclass(frozen = True)
class ToxicTriviaPunishment():
    cutenessResult: CutenessResult
    numberOfPunishments: int
    punishedByPoints: int
    userId: str
    userName: str

    @property
    def numberOfPunishmentsStr(self) -> str:
        return locale.format_string("%d", self.numberOfPunishments, grouping = True)

    @property
    def punishedByPointsStr(self) -> str:
        return locale.format_string("%d", self.punishedByPoints, grouping = True)
