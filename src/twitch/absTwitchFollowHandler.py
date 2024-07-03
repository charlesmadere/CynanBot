from abc import ABC, abstractmethod

from .api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..users.userInterface import UserInterface


class AbsTwitchFollowHandler(ABC):

    @abstractmethod
    async def onNewFollow(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass
