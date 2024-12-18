from abc import ABC, abstractmethod


class MicrosoftSamApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(self, text: str) -> bytes:
        pass
