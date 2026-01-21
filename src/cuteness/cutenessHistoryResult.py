import locale
from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessHistoryEntry import CutenessHistoryEntry
from ..misc import utils as utils


@dataclass(frozen = True, slots = True)
class CutenessHistoryResult:
    userId: str
    userName: str
    bestCuteness: CutenessHistoryEntry | None = None
    entries: FrozenList[CutenessHistoryEntry] | None = None
    totalCuteness: int | None = None

    def requireTotalCuteness(self) -> int:
        if not utils.isValidInt(self.totalCuteness):
            raise RuntimeError(f'No totalCuteness value is available: {self}')

        return self.totalCuteness

    @property
    def totalCutenessStr(self) -> str:
        totalCuteness = self.requireTotalCuteness()
        return locale.format_string("%d", totalCuteness, grouping = True)
