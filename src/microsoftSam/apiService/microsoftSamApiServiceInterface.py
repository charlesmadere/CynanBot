from abc import ABC, abstractmethod


class MicrosoftSamApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(self, text: str, voice: str, pitch: str, speed: str) -> bytes:
        pass
