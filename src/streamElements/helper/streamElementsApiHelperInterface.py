from abc import ABC, abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsApiHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None,
        twitchChannelId: str,
        voice: StreamElementsVoice,
    ) -> bytes | None:
        pass
