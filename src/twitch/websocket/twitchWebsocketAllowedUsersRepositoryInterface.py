from abc import ABC, abstractmethod

from .twitchWebsocketUser import TwitchWebsocketUser


class TwitchWebsocketAllowedUsersRepositoryInterface(ABC):

    @abstractmethod
    async def getUsers(self) -> frozenset[TwitchWebsocketUser]:
        pass
