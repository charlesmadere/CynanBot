from abc import ABC, abstractmethod

from CynanBot.tts.ttsEvent import TtsEvent


class TtsManagerInterface(ABC):

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playTtsEvent(self, event: TtsEvent) -> bool:
        pass
