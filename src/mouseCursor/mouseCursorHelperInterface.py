from abc import ABC, abstractmethod

from ..users.userInterface import UserInterface


class MouseCursorHelperInterface(ABC):

    @abstractmethod
    async def applyMouseCursor(
        self,
        twitchChannelId: str,
        twitchUser: UserInterface,
    ) -> bool:
        pass
