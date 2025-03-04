from abc import ABC, abstractmethod

from ..models.decTalkFileReference import DecTalkFileReference
from ..models.decTalkVoice import DecTalkVoice


class DecTalkHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voice: DecTalkVoice | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> DecTalkFileReference | None:
        pass

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> str | None:
        pass
