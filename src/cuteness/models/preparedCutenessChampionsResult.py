from dataclasses import dataclass

from frozenlist import FrozenList

from .preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessChampionsResult:
    champions: FrozenList[PreparedCutenessLeaderboardEntry]
    twitchChannelId: str
    twitchUser: UserInterface

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle
