from abc import ABC, abstractmethod

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
