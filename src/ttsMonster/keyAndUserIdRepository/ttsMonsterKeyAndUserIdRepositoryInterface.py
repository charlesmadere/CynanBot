from abc import abstractmethod

from .ttsMonsterKeyAndUserId import TtsMonsterKeyAndUserId
from ...misc.clearable import Clearable


class TtsMonsterKeyAndUserIdRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, twitchChannel: str) -> TtsMonsterKeyAndUserId | None:
        pass
