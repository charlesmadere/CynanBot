from abc import abstractmethod

from .ttsMonsterKeyAndUserId import TtsMonsterKeyAndUserId
from ...misc.clearable import Clearable


class TtsMonsterKeyAndUserIdRepositoryInterface(Clearable):

    # The data in this returned value correspond to the key and userId values that are sent via an
    # HTTP POST request to the following URL: https://us-central1-tts-monster.cloudfunctions.net/generateTTS
    @abstractmethod
    async def get(self, twitchChannel: str) -> TtsMonsterKeyAndUserId | None:
        pass
