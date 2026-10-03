from dataclasses import dataclass
from datetime import datetime

from .cutenessEntry import CutenessEntry
from .cutenessHistoryEntry import CutenessHistoryEntry
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessHistoryEntry(CutenessEntry, TwitchUserInterface):
    cutenessHistoryEntry: CutenessHistoryEntry
    chatterUserLogin: str
    chatterUserName: str

    @property
    def chatterUserId(self) -> str:
        return self.cutenessHistoryEntry.chatterUserId

    @property
    def cutenessDate(self) -> datetime:
        return self.cutenessHistoryEntry.cutenessDate

    def getChatterUserId(self) -> str:
        return self.cutenessHistoryEntry.getChatterUserId()

    def getCuteness(self) -> int:
        return self.cutenessHistoryEntry.cuteness

    def getTwitchChannelId(self) -> str:
        return self.cutenessHistoryEntry.twitchChannelId

    def getUserId(self) -> str:
        return self.cutenessHistoryEntry.getChatterUserId()

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName
