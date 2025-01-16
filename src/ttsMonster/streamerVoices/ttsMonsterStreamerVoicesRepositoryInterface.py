from abc import abstractmethod

from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc.clearable import Clearable


class TtsMonsterStreamerVoicesRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchVoices(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> frozenset[TtsMonsterVoice]:
        pass
