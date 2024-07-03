import locale
from dataclasses import dataclass

from ..misc import utils as utils
from .cutenessHistoryEntry import CutenessHistoryEntry


@dataclass(frozen = True)
class CutenessHistoryResult():
    userId: str
    userName: str
    bestCuteness: CutenessHistoryEntry | None = None
    totalCuteness: int | None = None
    entries: list[CutenessHistoryEntry] | None = None

    @property
    def totalCutenessStr(self) -> str:
        totalCuteness = self.requireTotalCuteness()
        return locale.format_string("%d", totalCuteness, grouping = True)

    def requireTotalCuteness(self) -> int:
        if not utils.isValidInt(self.totalCuteness):
            raise RuntimeError(f'No totalCuteness value is available: {self}')

        return self.totalCuteness
