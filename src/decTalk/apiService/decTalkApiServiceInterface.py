from abc import ABC, abstractmethod


class DecTalkApiServiceInterface(ABC):

    @abstractmethod
    async def generateSpeechFile(self, text: str) -> str:
        pass
