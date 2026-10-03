from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessHistoryResult import CutenessHistoryResult
from .preparedCutenessHistoryEntry import PreparedCutenessHistoryEntry


@dataclass(frozen = True, slots = True)
class PreparedCutenessHistoryResult:
    cutenessHistoryResult: CutenessHistoryResult
    historyEntries: FrozenList[PreparedCutenessHistoryEntry]
    bestCuteness: PreparedCutenessHistoryEntry | None

    @property
    def chatterUserId(self) -> str:
        return self.cutenessHistoryResult.chatterUserId

    def requireTotalCuteness(self) -> int:
        return self.cutenessHistoryResult.requireTotalCuteness()

    @property
    def totalCuteness(self) -> int | None:
        return self.cutenessHistoryResult.totalCuteness

    @property
    def totalCutenessStr(self) -> str:
        return self.cutenessHistoryResult.totalCutenessStr

    @property
    def twitchChannelId(self) -> str:
        return self.cutenessHistoryResult.twitchChannelId
