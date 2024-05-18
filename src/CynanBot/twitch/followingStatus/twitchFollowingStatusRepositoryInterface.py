from abc import abstractmethod
from datetime import datetime

from CynanBot.misc.clearable import Clearable
from CynanBot.twitch.followingStatus.twitchFollowingStatus import \
    TwitchFollowingStatus


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
