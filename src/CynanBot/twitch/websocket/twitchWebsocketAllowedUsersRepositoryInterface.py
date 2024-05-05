from abc import ABC, abstractmethod

from CynanBot.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser


class TwitchWebsocketAllowedUsersRepositoryInterface(ABC):

    @abstractmethod
    async def getUsers(self) -> set[TwitchWebsocketUser]:
        pass
