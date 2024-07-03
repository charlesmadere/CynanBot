from abc import abstractmethod

from .timeoutCheerActionHistory import \
    TimeoutCheerActionHistory
from ...misc.clearable import Clearable


class TimeoutCheerActionHistoryRepositoryInterface(Clearable):

    @abstractmethod
    async def add(
        self,
        bitAmount: int,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchAccessToken: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ):
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchAccessToken: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TimeoutCheerActionHistory | None:
        pass
