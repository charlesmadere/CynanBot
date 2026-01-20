from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchHypeTrainType import TwitchHypeTrainType
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..users.userInterface import UserInterface


class AbsTwitchHypeTrainHandler(ABC):

    @dataclass(frozen = True, slots = True)
    class HypeTrainData:
        isSharedTrain: bool
        level: int
        total: int
        hypeTrainId: str
        twitchChannelId: str
        hypeTrainType: TwitchHypeTrainType
        subscriptionType: TwitchWebsocketSubscriptionType
        user: UserInterface

    @abstractmethod
    async def onNewHypeTrain(self, hypeTrainData: HypeTrainData):
        pass

    @abstractmethod
    async def onNewHypeTrainDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
