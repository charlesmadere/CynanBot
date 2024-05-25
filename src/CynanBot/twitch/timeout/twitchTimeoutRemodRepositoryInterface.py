from abc import ABC, abstractmethod

from CynanBot.twitch.timeout.twitchTimeoutRemodData import \
    TwitchTimeoutRemodData


class TwitchTimeoutRemodRepositoryInterface(ABC):

    @abstractmethod
    async def add(self, data: TwitchTimeoutRemodData):
        pass

    @abstractmethod
    async def delete(self, broadcasterUserId: str, userId: str):
        pass

    @abstractmethod
    async def getAll(self) -> list[TwitchTimeoutRemodData]:
        pass
