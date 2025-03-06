from abc import ABC, abstractmethod

from ..models.ttsMonsterFileReference import TtsMonsterFileReference


class TtsMonsterHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterFileReference | None:
        pass
