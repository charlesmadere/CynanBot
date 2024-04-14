from abc import ABC, abstractmethod

from CynanBot.users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelperInterface(ABC):

    @abstractmethod
    async def checkMessageAndMaybeTimeout(
        self,
        chatterUserId: str,
        chatterUserName: str,
        message: str | None,
        twitchChannelId: str,
        user: UserInterface
    ):
        pass
