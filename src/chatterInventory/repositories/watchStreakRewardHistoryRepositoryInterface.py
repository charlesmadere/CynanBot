from abc import ABC, abstractmethod

from ..models.watchStreakRewardHistoryData import WatchStreakRewardHistoryData


class WatchStreakRewardHistoryRepositoryInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakRewardHistoryData | None:
        pass

    @abstractmethod
    async def update(
        self,
        watchStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        pass
