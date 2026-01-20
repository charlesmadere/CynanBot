import locale
from dataclasses import dataclass

from ...cuteness.incrementedCutenessResult import IncrementedCutenessResult


@dataclass(frozen = True, slots = True)
class ToxicTriviaPunishment:
    cutenessResult: IncrementedCutenessResult
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
