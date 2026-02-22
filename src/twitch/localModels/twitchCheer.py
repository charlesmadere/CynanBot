from dataclasses import dataclass

from .twitchUserInterface import TwitchUserInterface
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchCheer(TwitchUserInterface):
    bits: int
    chatMessage: str
    cheerUserId: str
    cheerUserLogin: str
    cheerUserName: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    twitchUser: UserInterface

    def getUserId(self) -> str:
        return self.cheerUserId

    def getUserLogin(self) -> str:
        return self.cheerUserLogin

    def getUserName(self) -> str:
        return self.cheerUserName

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle
