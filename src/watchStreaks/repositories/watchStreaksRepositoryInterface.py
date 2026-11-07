from abc import ABC, abstractmethod

from ..models.watchStreakStats import WatchStreakStats
from ...misc.clearable import Clearable


class WatchStreaksRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats | None:
        pass

    @abstractmethod
    async def update(
        self,
        currentStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats:
        pass
