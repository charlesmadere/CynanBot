from abc import ABC, abstractmethod

from ..models.ttsMonsterUrls import TtsMonsterUrls


class TtsMonsterPrivateApiHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        pass
