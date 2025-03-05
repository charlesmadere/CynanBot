from abc import ABC, abstractmethod

from ..models.decTalkVoice import DecTalkVoice


class DecTalkApiServiceInterface(ABC):

    @abstractmethod
    async def generateSpeechFile(
        self,
        voice: DecTalkVoice | None,
        text: str
    ) -> str:
        pass
