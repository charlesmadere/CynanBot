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
        user: UserInterface
    ) -> bool:
        pass
