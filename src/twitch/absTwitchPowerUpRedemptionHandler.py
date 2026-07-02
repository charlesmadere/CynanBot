from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .localModels.twitchPowerUpRedemption import TwitchPowerUpRedemption
from ..users.userInterface import UserInterface


class AbsTwitchPowerUpRedemptionHandler(ABC):

    @abstractmethod
    async def onNewPowerUpRedemption(self, powerUpRedemption: TwitchPowerUpRedemption):
        pass

    @abstractmethod
    async def onNewPowerUpRedemptionDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
