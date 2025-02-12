from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchChatHandler(ABC):

    @abstractmethod
    async def onNewChat(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
