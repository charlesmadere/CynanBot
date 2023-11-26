from abc import ABC, abstractmethod

from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchSubscriptionHandler(ABC):

    @abstractmethod
    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
