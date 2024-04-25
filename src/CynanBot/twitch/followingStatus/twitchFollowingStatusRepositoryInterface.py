from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.twitch.api.twitchFollower import TwitchFollower


class TwitchFollowingStatusRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchFollowingStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchFollower | None:
        pass
