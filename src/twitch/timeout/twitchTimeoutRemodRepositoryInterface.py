from abc import ABC, abstractmethod
from datetime import datetime

from frozenlist import FrozenList

from .twitchTimeoutRemodData import TwitchTimeoutRemodData


class TwitchTimeoutRemodRepositoryInterface(ABC):

    @abstractmethod
    async def add(
        self,
        remodDateTime: datetime,
        broadcasterUserId: str,
        userId: str,
    ):
        pass

    @abstractmethod
    async def delete(
        self,
        broadcasterUserId: str,
        userId: str,
    ):
        pass

    @abstractmethod
    async def getAll(self) -> FrozenList[TwitchTimeoutRemodData]:
        pass
