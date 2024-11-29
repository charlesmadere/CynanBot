from abc import ABC, abstractmethod

from .api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchSubscriptionHandler(ABC):

    @abstractmethod
    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass

    @abstractmethod
    def start(self):
        pass
