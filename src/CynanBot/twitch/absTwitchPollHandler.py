from abc import ABC, abstractmethod

from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchPollHandler(ABC):

    @abstractmethod
    async def onNewPoll(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
