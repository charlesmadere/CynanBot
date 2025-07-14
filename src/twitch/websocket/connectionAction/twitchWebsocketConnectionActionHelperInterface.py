from abc import ABC, abstractmethod

from .twitchWebsocketConnectionAction import TwitchWebsocketConnectionAction
from ..twitchWebsocketUser import TwitchWebsocketUser
from ...api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle


class TwitchWebsocketConnectionActionHelperInterface(ABC):

    @abstractmethod
    async def handleConnectionRelatedActions(
        self,
        dataBundle: TwitchWebsocketDataBundle,
        user: TwitchWebsocketUser,
    ) -> TwitchWebsocketConnectionAction:
        pass
