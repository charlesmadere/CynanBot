from abc import ABC, abstractmethod


class EccoApiServiceInterface(ABC):

    @abstractmethod
    async def fetchEccoWebsiteHtmlString(self) -> str:
        pass
