from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..misc.startable import Startable
from ..users.userInterface import UserInterface


class AbsTwitchChannelPointRedemptionHandler(Startable, ABC):

    @abstractmethod
    async def onNewChannelPointsRedemption(self, channelPointsRedemption: TwitchChannelPointsRedemption):
        pass

    @abstractmethod
    async def onNewChannelPointRedemptionDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
