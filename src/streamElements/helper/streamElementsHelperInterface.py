from abc import ABC, abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
        voice: StreamElementsVoice | None
    ) -> bytes | None:
        pass
