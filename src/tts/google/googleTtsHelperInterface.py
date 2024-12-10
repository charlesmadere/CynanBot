from abc import ABC, abstractmethod


class GoogleTtsHelperInterface(ABC):

    @abstractmethod
    async def getSpeechFile(self, message: str) -> str | None:
        pass
