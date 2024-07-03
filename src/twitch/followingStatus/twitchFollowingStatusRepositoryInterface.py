from abc import abstractmethod
from datetime import datetime

from .twitchFollowingStatus import TwitchFollowingStatus
from ...misc.clearable import Clearable


class TwitchFollowingStatusRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchFollowingStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchFollowingStatus | None:
        pass

    @abstractmethod
    async def persistFollowingStatus(
        self,
        followedAt: datetime | None,
        twitchChannelId: str,
        userId: str
    ):
        pass
