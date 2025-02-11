from abc import ABC, abstractmethod

from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ...tts.ttsProvider import TtsProvider


class GlacialTtsFileRetrieverInterface(ABC):

    @abstractmethod
    async def findFile(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference | None:
        pass

    @abstractmethod
    async def saveFile(
        self,
        fileExtension: str,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference:
        pass
