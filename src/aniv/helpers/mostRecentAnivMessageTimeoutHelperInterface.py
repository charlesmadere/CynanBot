from abc import ABC, abstractmethod

from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelperInterface(ABC):

    @abstractmethod
    async def checkMessageAndMaybeTimeout(
        self,
        chatterMessage: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        user: UserInterface,
    ) -> bool:
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
