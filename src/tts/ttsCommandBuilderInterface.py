from abc import ABC, abstractmethod

from .ttsEvent import TtsEvent
from .ttsProvider import TtsProvider


class TtsCommandBuilderInterface(ABC):

    @abstractmethod
    async def buildAndCleanEvent(self, event: TtsEvent | None) -> str | None:
        pass

    @abstractmethod
    async def buildAndCleanMessage(
        self,
        provider: TtsProvider,
        message: str | None
    ) -> str | None:
        pass
