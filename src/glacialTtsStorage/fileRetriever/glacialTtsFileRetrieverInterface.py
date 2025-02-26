from abc import ABC, abstractmethod

from ..models.glacialTtsFileReference import GlacialTtsFileReference
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsFileRetrieverInterface(ABC):

    @abstractmethod
    async def findFile(
        self,
        extraConfigurationData: str | None,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference | None:
        pass

    @abstractmethod
    async def saveFile(
        self,
        extraConfigurationData: str | None,
        fileExtension: str,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsFileReference:
        pass
