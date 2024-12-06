from abc import ABC, abstractmethod

from .ttsEvent import TtsEvent


class CompositeTtsManagerInterface(ABC):

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playTtsEvent(self, event: TtsEvent) -> bool:
        pass

    @abstractmethod
    async def stopTtsEvent(self):
        pass
