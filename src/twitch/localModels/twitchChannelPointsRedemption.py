from dataclasses import dataclass

from .twitchUserInterface import TwitchUserInterface
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchChannelPointsRedemption(TwitchUserInterface):
    rewardCost: int
    eventId: str
    redemptionMessage: str | None
    redemptionUserId: str
    redemptionUserLogin: str
    redemptionUserName: str
    rewardId: str
    twitchChannelId: str
    twitchUser: UserInterface

    def getUserId(self) -> str:
        return self.redemptionUserId

    def getUserLogin(self) -> str:
        return self.redemptionUserLogin

    def getUserName(self) -> str:
        return self.redemptionUserName

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle
