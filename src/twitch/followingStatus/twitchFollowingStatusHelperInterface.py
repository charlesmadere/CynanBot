from abc import ABC, abstractmethod

from .preparedTwitchFollowingStatus import PreparedTwitchFollowingStatus


class TwitchFollowingStatusHelperInterface(ABC):

    @abstractmethod
    async def fetch(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> PreparedTwitchFollowingStatus | None:
        pass
