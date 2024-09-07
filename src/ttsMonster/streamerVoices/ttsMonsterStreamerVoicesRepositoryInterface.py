from abc import abstractmethod
from typing import Collection

from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc.clearable import Clearable


class TtsMonsterStreamerVoicesRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchVoices(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> Collection[TtsMonsterVoice]:
        pass
