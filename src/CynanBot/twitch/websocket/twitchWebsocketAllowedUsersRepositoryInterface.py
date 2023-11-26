from abc import ABC, abstractmethod
from typing import Set

from CynanBot.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser


class TwitchWebsocketAllowedUsersRepositoryInterface(ABC):

    @abstractmethod
    async def getUsers(self) -> Set[TwitchWebsocketUser]:
        pass
