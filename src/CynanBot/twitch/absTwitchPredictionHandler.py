from abc import ABC, abstractmethod

from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface


class AbsTwitchPredictionHandler(ABC):

    @abstractmethod
    async def onNewPrediction(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
