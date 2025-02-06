from abc import ABC, abstractmethod

from ...tts.ttsProvider import TtsProvider


class GlacialTtsIdGeneratorInterface(ABC):

    @abstractmethod
    async def generateId(
        self,
        message: str,
        provider: TtsProvider
    ) -> str:
        pass
