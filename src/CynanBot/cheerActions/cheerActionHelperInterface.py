from abc import ABC, abstractmethod

from CynanBot.users.userInterface import UserInterface


class CheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        user: UserInterface
    ) -> bool:
        pass
