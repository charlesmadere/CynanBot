from dataclasses import dataclass

from .twitchCustomPowerUpData import TwitchCustomPowerUpData
from .twitchUserInterface import TwitchUserInterface
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchBitsUse(TwitchUserInterface):
    bits: int
    bitsUserId: str
    bitsUserLogin: str
    bitsUserName: str
    eventId: str
    twitchChannelId: str
    customPowerUpData: TwitchCustomPowerUpData | None
    twitchUser: UserInterface

    def getUserId(self) -> str:
        return self.bitsUserId

    def getUserLogin(self) -> str:
        return self.bitsUserLogin

    def getUserName(self) -> str:
        return self.bitsUserName
