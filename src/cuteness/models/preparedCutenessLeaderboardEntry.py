from dataclasses import dataclass

from .cutenessEntry import CutenessEntry
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessLeaderboardEntry(CutenessEntry):
    cutenessLeaderboardEntry: CutenessLeaderboardEntry
    chatterUserName: str
    twitchUser: UserInterface

    def getChatterUserId(self) -> str:
        return self.cutenessLeaderboardEntry.getChatterUserId()

    def getCuteness(self) -> int:
        return self.cutenessLeaderboardEntry.getCuteness()

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle
