import locale
from dataclasses import dataclass

from .cutenessDate import CutenessDate
from ..misc import utils as utils


@dataclass(frozen = True)
class IncrementedCutenessResult:
    cutenessDate: CutenessDate
    cuteness: int
    previousCuteness: int | None
    userId: str
    userName: str

    @property
    def cutenessStr(self) -> str:
        return locale.format_string("%d", self.cuteness, grouping = True)

    @property
    def previousCutenessStr(self) -> str:
        previousCuteness = self.requirePreviousCuteness()
        return locale.format_string("%d", previousCuteness, grouping = True)

    def requirePreviousCuteness(self) -> int:
        if not utils.isValidInt(self.previousCuteness):
            raise RuntimeError(f'No previous cuteness value is available: {self}')

        return self.previousCuteness
