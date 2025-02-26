from abc import ABC, abstractmethod

from .models.ttsEvent import TtsEvent
from .models.ttsProvider import TtsProvider


class TtsManagerInterface(ABC):

    @property
    @abstractmethod
    def isLoadingOrPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playTtsEvent(self, event: TtsEvent):
        pass

    @abstractmethod
    async def stopTtsEvent(self):
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
