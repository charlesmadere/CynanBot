from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .localModels.twitchCheer import TwitchCheer
from ..users.userInterface import UserInterface


class AbsTwitchCheerHandler(ABC):

    @abstractmethod
    async def onNewCheer(self, cheer: TwitchCheer):
        pass

    @abstractmethod
    async def onNewCheerDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
