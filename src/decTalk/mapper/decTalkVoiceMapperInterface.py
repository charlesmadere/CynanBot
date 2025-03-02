from abc import ABC, abstractmethod

from ..models.decTalkVoice import DecTalkVoice


class DecTalkVoiceMapperInterface(ABC):

    @abstractmethod
    async def fromString(self, voice: str) -> DecTalkVoice:
        pass

    @abstractmethod
    async def toString(self, voice: DecTalkVoice) -> str:
        pass
