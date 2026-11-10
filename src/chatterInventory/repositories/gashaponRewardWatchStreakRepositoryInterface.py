from abc import ABC, abstractmethod


class GashaponRewardWatchStreakRepositoryInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> int | None:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    async def set(
        self,
        watchStreak: int | None,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        pass
