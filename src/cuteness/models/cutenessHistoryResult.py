import locale
from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessHistoryEntry import CutenessHistoryEntry


@dataclass(frozen = True, slots = True)
class CutenessHistoryResult:
    bestCuteness: CutenessHistoryEntry | None
    historyEntries: FrozenList[CutenessHistoryEntry]
    totalCuteness: int | None
    chatterUserId: str
    twitchChannelId: str

    def requireTotalCuteness(self) -> int:
        if self.totalCuteness is None:
            raise RuntimeError(f'No totalCuteness value is available ({self=})')

        return self.totalCuteness

    @property
    def totalCutenessStr(self) -> str:
        totalCuteness = self.requireTotalCuteness()
        return locale.format_string("%d", totalCuteness, grouping = True)
