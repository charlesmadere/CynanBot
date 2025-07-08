from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchChatHandler(ABC):

    @abstractmethod
    async def onNewChat(
        self,
        bits: int | None,
        chatMessage: str,
        chatterUserId: str,
        chatterUserLogin: str,
        chatterUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ):
        pass

    @abstractmethod
    async def onNewChatDataBundle(
        self,
        broadcasterUserId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
