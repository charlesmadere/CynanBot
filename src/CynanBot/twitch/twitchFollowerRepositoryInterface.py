from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.twitch.api.twitchFollower import TwitchFollower


class TwitchFollowerRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchFollowingInfo(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchFollower | None:
        pass
