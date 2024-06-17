from abc import abstractmethod
from CynanBot.misc.clearable import Clearable

from CynanBot.cheerActions.timeout.timeoutCheerActionHistory import \
    TimeoutCheerActionHistory


class TimeoutCheerActionHistoryRepositoryInterface(Clearable):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchAccessToken: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerActionHistory | None:
        pass
