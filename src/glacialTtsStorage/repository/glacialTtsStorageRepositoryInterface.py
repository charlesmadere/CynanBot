from abc import ABC, abstractmethod

from ..models.glacialTtsData import GlacialTtsData
from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsStorageRepositoryInterface(ABC):

    @abstractmethod
    async def add(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsData:
        pass

    @abstractmethod
    async def get(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> GlacialTtsData | None:
        pass

    @abstractmethod
    async def remove(
        self,
        glacialId: str,
        provider: TtsProvider,
    ) -> GlacialTtsData | None:
        pass
