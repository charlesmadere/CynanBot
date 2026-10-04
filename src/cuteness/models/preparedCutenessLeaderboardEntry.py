from dataclasses import dataclass

from .cutenessEntry import CutenessEntry
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessLeaderboardEntry(CutenessEntry, TwitchUserInterface):
    cutenessLeaderboardEntry: CutenessLeaderboardEntry
    chatterUserLogin: str
    chatterUserName: str

    @property
    def chatterUserId(self) -> str:
        return self.getChatterUserId()

    @property
    def cuteness(self) -> int:
        return self.getCuteness()

    def getChatterUserId(self) -> str:
        return self.cutenessLeaderboardEntry.getChatterUserId()

    def getCuteness(self) -> int:
        return self.cutenessLeaderboardEntry.getCuteness()

    def getTwitchChannelId(self) -> str:
        return self.cutenessLeaderboardEntry.getTwitchChannelId()

    def getUserId(self) -> str:
        return self.cutenessLeaderboardEntry.getChatterUserId()

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName

    @property
    def rank(self) -> int:
        return self.cutenessLeaderboardEntry.rank

    @property
    def rankStr(self) -> str:
        return self.cutenessLeaderboardEntry.rankStr

    @property
    def twitchChannelId(self) -> str:
        return self.getTwitchChannelId()
