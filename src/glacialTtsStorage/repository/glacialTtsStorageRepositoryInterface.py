from abc import ABC, abstractmethod

from ..models.glacialTtsData import GlacialTtsData
from ...tts.ttsProvider import TtsProvider


class GlacialTtsStorageRepositoryInterface(ABC):

    @abstractmethod
    async def add(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsData:
        pass

    @abstractmethod
    async def get(
        self,
        message: str,
        provider: TtsProvider
    ) -> GlacialTtsData | None:
        pass

    @abstractmethod
    async def remove(
        self,
        glacialId: str
    ) -> GlacialTtsData | None:
        pass
