from abc import ABC, abstractmethod

from .ttsMonsterKeyAndUserId import TtsMonsterKeyAndUserId
from ...misc.clearable import Clearable


class TtsMonsterKeyAndUserIdRepositoryInterface(Clearable, ABC):

    # The data in this returned value correspond to the key and userId values that are sent via an
    # HTTP POST request to the following URL: https://us-central1-tts-monster.cloudfunctions.net/generateTTS
    @abstractmethod
    async def get(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterKeyAndUserId | None:
        pass
