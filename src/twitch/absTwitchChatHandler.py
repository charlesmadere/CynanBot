from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchChatMessage import TwitchChatMessage
from .api.models.twitchCheerMetadata import TwitchCheerMetadata
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..users.userInterface import UserInterface


class AbsTwitchChatHandler(ABC):

    @dataclass(frozen = True)
    class ChatData:
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str
        twitchChannelId: str
        twitchChatMessageId: str | None
        message: TwitchChatMessage
        cheer: TwitchCheerMetadata | None
        user: UserInterface

    @abstractmethod
    async def onNewChat(self, chatData: ChatData):
        pass

    @abstractmethod
    async def onNewChatDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
