from abc import ABC, abstractmethod

from ..models.ttsChatter import TtsChatter
from ...misc.clearable import Clearable


class TtsChatterRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> TtsChatter | None:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> TtsChatter | None:
        pass

    @abstractmethod
    async def set(self, ttsChatter: TtsChatter):
        pass
