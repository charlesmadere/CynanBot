from abc import ABC, abstractmethod

from ...users.userInterface import UserInterface


class BattleshipTimeoutHelperInterface(ABC):

    @abstractmethod
    async def fire(
        self,
        broadcasterUserId: str,
        originUserId: str,
        originUserName: str,
        user: UserInterface
    ) -> bool:
        pass
