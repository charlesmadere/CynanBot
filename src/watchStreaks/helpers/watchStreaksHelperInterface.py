from abc import ABC, abstractmethod

from ..models.watchStreakTtsAnnouncementResult import WatchStreakTtsAnnouncementResult
from ...users.userInterface import UserInterface


class WatchStreaksHelperInterface(ABC):

    @abstractmethod
    async def watchStreakTtsAnnounce(
        self,
        watchStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
        user: UserInterface,
    ) -> WatchStreakTtsAnnouncementResult:
        pass
