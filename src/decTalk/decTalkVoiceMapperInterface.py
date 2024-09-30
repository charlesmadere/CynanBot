from abc import ABC, abstractmethod

from .decTalkVoice import DecTalkVoice


class DecTalkVoiceMapperInterface(ABC):

    @abstractmethod
    async def toString(self, voice: DecTalkVoice) -> str:
        pass
