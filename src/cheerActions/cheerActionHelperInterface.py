from abc import ABC, abstractmethod

from ..users.userInterface import UserInterface


class CheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        pass
