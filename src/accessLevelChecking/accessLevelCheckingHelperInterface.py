from abc import ABC, abstractmethod

from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.accessLevel.accessLevel import AccessLevel


class AccessLevelCheckingHelperInterface(ABC):

    @abstractmethod
    async def checkStatus(
        self,
        requiredAccessLevel: AccessLevel,
        twitchMessage: TwitchMessage,
    ) -> bool:
        pass
