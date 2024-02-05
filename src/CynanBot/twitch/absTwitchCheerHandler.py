from abc import ABC, abstractmethod

from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchCheerHandler(ABC):

    @abstractmethod
    async def onNewCheer(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass
