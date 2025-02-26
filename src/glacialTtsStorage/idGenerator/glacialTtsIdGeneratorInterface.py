from abc import ABC, abstractmethod

from ...tts.models.ttsProvider import TtsProvider


class GlacialTtsIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateId(
        self,
        message: str,
        provider: TtsProvider
    ) -> str:
        pass
