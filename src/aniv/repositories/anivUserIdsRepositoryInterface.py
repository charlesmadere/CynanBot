from abc import ABC, abstractmethod

from frozendict import frozendict

from ..models.whichAnivUser import WhichAnivUser


class AnivUserIdsRepositoryInterface(ABC):

    @abstractmethod
    async def getAcacUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAllUserIds(self) -> frozendict[WhichAnivUser, str | None]:
        pass

    @abstractmethod
    async def getAneevUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAnivUserId(self) -> str | None:
        pass
