from abc import ABC, abstractmethod

from frozendict import frozendict

from ..models.whichAnivUser import WhichAnivUser


class AnivUserIdsRepositoryInterface(ABC):

    @abstractmethod
    async def determineAnivUser(
        self,
        chatterUserId: str | None,
    ) -> WhichAnivUser | None:
        pass

    @abstractmethod
    async def getAcacUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAlbeeevUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAllUsers(self) -> frozendict[WhichAnivUser, str | None]:
        pass

    @abstractmethod
    async def getAneevUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAnivUserId(self) -> str | None:
        pass
