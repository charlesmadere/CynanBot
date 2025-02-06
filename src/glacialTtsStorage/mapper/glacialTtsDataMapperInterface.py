from abc import ABC, abstractmethod

from ...tts.ttsProvider import TtsProvider


class GlacialTtsDataMapperInterface(ABC):

    @abstractmethod
    async def fromDatabaseName(self, ttsProvider: str) -> TtsProvider:
        pass

    @abstractmethod
    async def toDatabaseName(self, ttsProvider: TtsProvider) -> str:
        pass
