from abc import ABC, abstractmethod

from CynanBot.tts.ttsEvent import TtsEvent


class TtsManagerInterface(ABC):

    @abstractmethod
    async def isExecuting(self) -> bool:
        pass

    @abstractmethod
    async def playTtsEvent(self, event: TtsEvent):
        pass
