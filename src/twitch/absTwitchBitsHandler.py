from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .localModels.twitchBitsUse import TwitchBitsUse
from ..users.userInterface import UserInterface


class AbsTwitchBitsHandler(ABC):

    @abstractmethod
    async def onNewBits(self, bitsUse: TwitchBitsUse):
        pass

    @abstractmethod
    async def onNewBitsDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
