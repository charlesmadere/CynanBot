from dataclasses import dataclass

from .twitchUserInterface import TwitchUserInterface
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchChannelPointsRedemption(TwitchUserInterface):
    rewardCost: int
    eventId: str
    redemptionMessage: str | None
    rewardId: str
    twitchChannelId: str
    redemptionUserId: str
    redemptionUserLogin: str
    redemptionUserName: str
    twitchUser: UserInterface

    def getUserId(self) -> str:
        return self.redemptionUserId

    def getUserLogin(self) -> str:
        return self.redemptionUserLogin

    def getUserName(self) -> str:
        return self.redemptionUserName
