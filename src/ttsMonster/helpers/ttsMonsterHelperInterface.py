from abc import ABC, abstractmethod

from ..models.ttsMonsterFileReference import TtsMonsterFileReference
from ..models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
        voice: TtsMonsterVoice | None,
    ) -> TtsMonsterFileReference | None:
        pass
