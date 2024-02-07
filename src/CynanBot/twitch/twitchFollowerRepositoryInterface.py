from abc import abstractmethod
from typing import Optional

from CynanBot.misc.clearable import Clearable
from CynanBot.twitch.api.twitchFollower import TwitchFollower


class TwitchFollowerRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchFollowingInfo(
        self,
        twitchAccessToken: Optional[str],
        twitchChannelId: str,
        userId: str
    ) -> Optional[TwitchFollower]:
        pass
