from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchChatMessage import TwitchChatMessage
from .api.models.twitchChatMessageType import TwitchChatMessageType
from .api.models.twitchCheerMetadata import TwitchCheerMetadata
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
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
        messageType: TwitchChatMessageType
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

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
