from abc import ABC, abstractmethod

from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateId(
        self,
        message: str,
        voice: str | None,
        provider: TtsProvider,
    ) -> str:
        pass
