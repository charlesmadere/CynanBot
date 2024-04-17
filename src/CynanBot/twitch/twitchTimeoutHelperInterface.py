from abc import ABC, abstractmethod

from CynanBot.users.userInterface import UserInterface


class TwitchTimeoutHelperInterface(ABC):

    @abstractmethod
    async def timeout(
        self,
        reason: str | None,
        twitchAccessToken: str,
        twitchChannelId: str,
        userIdToTimeout: str,
        user: UserInterface
    ) -> bool:
        pass
