from abc import ABC, abstractmethod


class PuptimeUserIdProviderInterface(ABC):

    @abstractmethod
    async def getPuptimeUserId(self) -> str | None:
        pass
