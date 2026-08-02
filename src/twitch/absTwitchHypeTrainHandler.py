from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .localModels.twitchHypeTrainState import TwitchHypeTrainState
from .localModels.twitchHypeTrainType import TwitchHypeTrainType
from ..users.userInterface import UserInterface


class AbsTwitchHypeTrainHandler(ABC):

    @dataclass(frozen = True, slots = True)
    class HypeTrainData:
        isSharedTrain: bool
        level: int
        total: int
        hypeEmoji: str
        hypeTrainId: str
        twitchChannelId: str
        hypeTrainState: TwitchHypeTrainState
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
