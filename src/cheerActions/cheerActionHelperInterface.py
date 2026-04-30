from abc import ABC, abstractmethod

from ..misc.startable import Startable
from ..users.userInterface import UserInterface


class CheerActionHelperInterface(Startable, ABC):

    @abstractmethod
    async def handleCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        pass
