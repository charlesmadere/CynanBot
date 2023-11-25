from abc import ABC, abstractmethod

from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface


class AbsTwitchRaidHandler(ABC):

    @abstractmethod
    async def onNewRaid(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
