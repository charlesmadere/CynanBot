from abc import ABC, abstractmethod

from .ttsEvent import TtsEvent


class CompositeTtsManagerInterface(ABC):

    @property
    @abstractmethod
    def isLoadingOrPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playTtsEvent(self, event: TtsEvent) -> bool:
        pass

    @abstractmethod
    async def stopTtsEvent(self):
        pass
