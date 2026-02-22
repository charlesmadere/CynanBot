from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchChatMessageFragment import TwitchChatMessageFragment
from .twitchCheer import TwitchCheer
from .twitchUserInterface import TwitchUserInterface
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class TwitchChatMessage(TwitchUserInterface):
    twitchChatMessageFragments: FrozenList[TwitchChatMessageFragment]
    chatterUserId: str
    chatterUserLogin: str
    chatterUserName: str
    eventId: str
    sourceMessageId: str | None
    text: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    twitchCheer: TwitchCheer | None
    twitchUser: UserInterface

    def getUserId(self) -> str:
        return self.chatterUserId

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName

    @property
    def twitchChannel(self) -> str:
        return self.twitchUser.handle
