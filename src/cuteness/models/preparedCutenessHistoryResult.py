from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessHistoryResult import CutenessHistoryResult
from .preparedCutenessHistoryEntry import PreparedCutenessHistoryEntry
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessHistoryResult(TwitchUserInterface):
    cutenessHistoryResult: CutenessHistoryResult
    historyEntries: FrozenList[PreparedCutenessHistoryEntry]
    bestCuteness: PreparedCutenessHistoryEntry | None
    chatterUserLogin: str
    chatterUserName: str

    @property
    def chatterUserId(self) -> str:
        return self.cutenessHistoryResult.chatterUserId

    def getUserId(self) -> str:
        return self.cutenessHistoryResult.chatterUserId

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName

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
