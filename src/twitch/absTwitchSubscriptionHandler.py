from abc import ABC, abstractmethod

from .api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
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
