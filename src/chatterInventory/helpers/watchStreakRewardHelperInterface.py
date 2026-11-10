from abc import ABC, abstractmethod

from ...users.userInterface import UserInterface


class WatchStreakRewardHelperInterface(ABC):

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
