from abc import ABC, abstractmethod

from ..users.userInterface import UserInterface


class CheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleCheerAction(
        self,
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ) -> bool:
        pass
