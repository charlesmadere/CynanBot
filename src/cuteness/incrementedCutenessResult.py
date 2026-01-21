import locale
from dataclasses import dataclass

from .cutenessDate import CutenessDate


@dataclass(frozen = True, slots = True)
class IncrementedCutenessResult:
    cutenessDate: CutenessDate
    newCuteness: int
    previousCuteness: int
    userId: str
    userName: str

    @property
    def newCutenessStr(self) -> str:
        return locale.format_string("%d", self.newCuteness, grouping = True)

    @property
    def previousCutenessStr(self) -> str:
        return locale.format_string("%d", self.previousCuteness, grouping = True)
