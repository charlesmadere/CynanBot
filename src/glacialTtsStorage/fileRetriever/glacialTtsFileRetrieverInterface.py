from abc import ABC, abstractmethod

from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsFileRetrieverInterface(ABC):

    @abstractmethod
    async def findFile(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsFileReference | None:
        pass

    @abstractmethod
    async def saveFile(
        self,
        fileExtension: str,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsFileReference:
        pass
