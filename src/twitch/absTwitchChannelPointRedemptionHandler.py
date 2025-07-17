from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchChannelPointRedemptionHandler(ABC):

    @abstractmethod
    async def onNewChannelPointRedemption(self, channelPointsMessage: TwitchChannelPointsMessage):
        pass

    @abstractmethod
    async def onNewChannelPointRedemptionDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass

    @abstractmethod
    def start(self):
        pass
