from abc import ABC, abstractmethod

from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface


class AbsTwitchCheerHandler(ABC):

    @abstractmethod
    async def onNewCheer(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
