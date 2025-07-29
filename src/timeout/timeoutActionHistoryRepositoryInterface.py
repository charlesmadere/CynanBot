from abc import ABC, abstractmethod

from .timeoutActionHistory import TimeoutActionHistory
from ..misc.clearable import Clearable


class TimeoutActionHistoryRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def add(
        self,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> TimeoutActionHistory:
        pass
