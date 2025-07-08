from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchCheerHandler(ABC):

    @abstractmethod
    async def onNewCheer(
        self,
        bits: int,
        chatMessage: str,
        cheerUserId: str,
        cheerUserLogin: str,
        cheerUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ):
        pass

    @abstractmethod
    async def onNewCheerDataBundle(
        self,
        broadcasterUserId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
