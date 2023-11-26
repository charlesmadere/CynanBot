from abc import ABC, abstractmethod

from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchRaidHandler(ABC):

    @abstractmethod
    async def onNewRaid(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
