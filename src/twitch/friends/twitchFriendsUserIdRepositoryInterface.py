from abc import ABC, abstractmethod


class TwitchFriendsUserIdRepositoryInterface(ABC):

    @abstractmethod
    async def getAlbeeesUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getCharlesUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getEddieUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getHokkaidoubareUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getImytUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getMandooBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getOathyBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getStashiocatUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getVolwrathUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getZanianUserId(self) -> str | None:
        pass
