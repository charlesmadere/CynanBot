from dataclasses import dataclass

from .cutenessEntry import CutenessEntry
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessLeaderboardEntry(CutenessEntry):
    cutenessLeaderboardEntry: CutenessLeaderboardEntry
    chatterUserName: str
    twitchUser: UserInterface

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

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle

    @property
    def twitchChannelId(self) -> str:
        return self.getTwitchChannelId()
