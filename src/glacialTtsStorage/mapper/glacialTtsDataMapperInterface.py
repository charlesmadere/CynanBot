from abc import ABC, abstractmethod

from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsDataMapperInterface(ABC):

    @abstractmethod
    async def fromDatabaseName(self, ttsProvider: str) -> TtsProvider:
        pass

    @abstractmethod
    async def toDatabaseName(self, ttsProvider: TtsProvider) -> str:
        pass

    @abstractmethod
    async def toFolderName(self, ttsProvider: TtsProvider) -> str:
        pass
