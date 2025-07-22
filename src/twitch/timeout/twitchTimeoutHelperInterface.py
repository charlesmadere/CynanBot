from abc import ABC, abstractmethod

from .twitchTimeoutResult import TwitchTimeoutResult
from ...users.userInterface import UserInterface


class TwitchTimeoutHelperInterface(ABC):

    @abstractmethod
    async def timeout(
        self,
        durationSeconds: int,
        reason: str | None,
        twitchAccessToken: str,
        twitchChannelAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        user: UserInterface,
    ) -> TwitchTimeoutResult:
        pass
