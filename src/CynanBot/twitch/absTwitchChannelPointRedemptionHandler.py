from abc import ABC, abstractmethod

from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface


class AbsTwitchChannelPointRedemptionHandler(ABC):

    @abstractmethod
    async def onNewChannelPointRedemption(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        pass
