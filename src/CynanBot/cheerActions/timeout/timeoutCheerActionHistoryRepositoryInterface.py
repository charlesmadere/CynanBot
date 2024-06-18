from abc import abstractmethod
from CynanBot.misc.clearable import Clearable

from CynanBot.cheerActions.timeout.timeoutCheerActionHistory import \
    TimeoutCheerActionHistory


class TimeoutCheerActionHistoryRepositoryInterface(Clearable):

    @abstractmethod
    async def add(
        self,
        bitAmount: int,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchAccessToken: str | None,
        twitchChannelId: str
    ):
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchAccessToken: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerActionHistory | None:
        pass
