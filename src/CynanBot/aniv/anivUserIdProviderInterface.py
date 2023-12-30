from abc import ABC, abstractmethod


class AnivUserIdProviderInterface(ABC):

    @abstractmethod
    async def getAnivUserId(self) -> str:
        pass
