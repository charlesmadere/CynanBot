from abc import ABC, abstractmethod

from ..models.glacialTtsData import GlacialTtsData
from ...tts.ttsProvider import TtsProvider


class GlacialTtsFileRetrieverInterface(ABC):

    @abstractmethod
    async def findFile(
        self,
        glacialData: GlacialTtsData
    ) -> str | None:
        pass

    @abstractmethod
    async def saveFile(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsData:
        pass
