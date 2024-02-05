from abc import ABC, abstractmethod

from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchChannelPointRedemptionHandler(ABC):

    @abstractmethod
    async def onNewChannelPointRedemption(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass
