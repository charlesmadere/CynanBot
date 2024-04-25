from abc import abstractmethod

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
