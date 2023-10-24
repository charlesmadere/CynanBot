from abc import ABC, abstractmethod

from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface


class AbsTwitchSubscriptionHandler(ABC):

    @abstractmethod
    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
