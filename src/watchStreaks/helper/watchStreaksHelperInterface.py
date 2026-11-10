from abc import ABC, abstractmethod

from ..models.announceWatchStreakResult import AnnounceWatchStreakResult
from ..models.watchStreakStats import WatchStreakStats
from ...users.userInterface import UserInterface


class WatchStreaksHelperInterface(ABC):

    @abstractmethod
    async def announceWatchStreak(
        self,
        watchStreak: int,
        chatterUserId: str,
        chatterUserLogin: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface,
    ) -> AnnounceWatchStreakResult:
        pass

    @abstractmethod
    async def requestWatchStreakReward(
        self,
        watchStreak: int,
        chatMessage: str | None,
        chatterUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        pass

    @abstractmethod
    async def updateWatchStreakStats(
        self,
        watchStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats:
        pass
