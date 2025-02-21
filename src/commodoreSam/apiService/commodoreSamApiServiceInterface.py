from abc import ABC, abstractmethod


class CommodoreSamApiServiceInterface(ABC):

    @abstractmethod
    async def generateSpeechFile(self, text: str) -> str:
        pass
