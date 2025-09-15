from abc import ABC, abstractmethod
from datetime import datetime

from .twitchFollowingStatus import TwitchFollowingStatus
from ...misc.clearable import Clearable


class TwitchFollowingStatusRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchFollowingStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str,
    ) -> TwitchFollowingStatus | None:
        pass

    @abstractmethod
    async def isFollowing(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str,
    ) -> bool:
        pass

    @abstractmethod
    async def persistFollowingStatus(
        self,
        followedAt: datetime | None,
        twitchChannelId: str,
        userId: str,
    ):
        pass
