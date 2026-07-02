from dataclasses import dataclass

from .twitchCustomPowerUp import TwitchCustomPowerUp
from .twitchUserInterface import TwitchUserInterface
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchPowerUpRedemption(TwitchUserInterface):
    eventId: str
    redemptionMessage: str | None
    redemptionUserId: str
    redemptionUserLogin: str
    redemptionUserName: str
    twitchChannelId: str
    customPowerUp: TwitchCustomPowerUp
    twitchUser: UserInterface

    @property
    def bits(self) -> int:
        return self.customPowerUp.bits

    def getUserId(self) -> str:
        return self.redemptionUserId

    def getUserLogin(self) -> str:
        return self.redemptionUserLogin

    def getUserName(self) -> str:
        return self.redemptionUserName

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle
