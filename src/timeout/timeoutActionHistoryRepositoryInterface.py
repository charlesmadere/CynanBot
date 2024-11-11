from abc import abstractmethod

from .timeoutActionHistory import TimeoutActionHistory
from ..misc.clearable import Clearable


class TimeoutActionHistoryRepositoryInterface(Clearable):

    @abstractmethod
    async def add(
        self,
        bitAmount: int,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TimeoutActionHistory:
        pass
