from abc import ABC, abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsMessageVoiceParserInterface(ABC):

    @abstractmethod
    async def determineVoiceFromMessage(self, message: str) -> StreamElementsVoice | None:
        pass
