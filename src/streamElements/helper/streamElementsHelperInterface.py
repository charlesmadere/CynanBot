from abc import ABC, abstractmethod

from ..models.StreamElementsFileReference import StreamElementsFileReference
from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
        voice: StreamElementsVoice | None
    ) -> StreamElementsFileReference | None:
        pass
