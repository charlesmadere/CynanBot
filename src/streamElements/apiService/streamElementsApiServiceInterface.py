from abc import ABC, abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsApiServiceInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        voice: StreamElementsVoice,
        text: str,
        userKey: str
    ) -> bytes:
        pass
