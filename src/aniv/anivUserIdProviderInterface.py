from abc import ABC, abstractmethod


class AnivUserIdProviderInterface(ABC):

    @abstractmethod
    async def getAneevUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAnivUserId(self) -> str | None:
        pass
