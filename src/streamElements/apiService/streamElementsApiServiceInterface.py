from abc import ABC, abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        text: str,
        userKey: str,
        voice: StreamElementsVoice,
    ) -> bytes:
        pass
