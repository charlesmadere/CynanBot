from abc import ABC, abstractmethod


class GoogleProjectIdProviderInterface(ABC):

    @abstractmethod
    async def getGoogleProjectId(self) -> str:
        pass
