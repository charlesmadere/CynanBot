from abc import ABC, abstractmethod


class CommodoreSamHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> str | None:
        pass
