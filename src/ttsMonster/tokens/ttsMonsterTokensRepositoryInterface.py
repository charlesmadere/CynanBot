from abc import ABC, abstractmethod

from ..models.ttsMonsterTokens import TtsMonsterTokens
from ...misc.clearable import Clearable


class TtsMonsterTokensRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        twitchChannelId: str,
    ) -> TtsMonsterTokens | None:
        pass

    @abstractmethod
    async def set(
        self,
        ttsMonsterKey: str | None,
        ttsMonsterUserId: str | None,
        twitchChannelId: str,
    ):
        pass
