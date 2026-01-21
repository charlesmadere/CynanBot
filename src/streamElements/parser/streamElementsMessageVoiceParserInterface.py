from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsMessageVoiceParserInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        message: str
        voice: StreamElementsVoice

    @abstractmethod
    async def determineVoiceFromMessage(
        self,
        message: str | None,
    ) -> Result | None:
        pass
