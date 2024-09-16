from abc import ABC, abstractmethod

from ..models.ttsMonsterUrls import TtsMonsterUrls


class TtsMonsterHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        pass
