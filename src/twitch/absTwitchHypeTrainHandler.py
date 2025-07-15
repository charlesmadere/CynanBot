from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchHypeTrainType import TwitchHypeTrainType
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchHypeTrainHandler(ABC):

    @dataclass(frozen = True)
    class HypeTrainData:
        isSharedTrain: bool
        level: int
        total: int
        twitchChannelId: str
        hypeTrainType: TwitchHypeTrainType
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

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
