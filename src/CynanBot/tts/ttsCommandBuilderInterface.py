from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.tts.ttsEvent import TtsEvent


class TtsCommandBuilderInterface(ABC):

    @abstractmethod
    async def buildAndCleanEvent(self, event: Optional[TtsEvent]) -> Optional[str]:
        pass

    @abstractmethod
    async def buildAndCleanMessage(self, message: Optional[str]) -> Optional[str]:
        pass
