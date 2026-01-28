from abc import ABC, abstractmethod

from ..models.streamElementsFileReference import StreamElementsFileReference
from ..models.streamElementsVoice import StreamElementsVoice


class StreamElementsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        donationPrefix: str | None,
        message: str | None,
        twitchChannelId: str,
        voice: StreamElementsVoice | None,
    ) -> StreamElementsFileReference | None:
        pass
