from abc import abstractmethod
from typing import List

from misc.clearable import Clearable
from users.userInterface import UserInterface


class UsersRepositoryInterface(Clearable):

    @abstractmethod
    async def addUser(self, handle: str):
        pass

    @abstractmethod
    def containsUser(self, handle: str) -> bool:
        pass

    @abstractmethod
    async def containsUserAsync(self, handle: str) -> bool:
        pass

    @abstractmethod
    def getUser(self, handle: str) -> UserInterface:
        pass

    @abstractmethod
    async def getUserAsync(self, handle: str) -> UserInterface:
        pass

    @abstractmethod
    def getUsers(self) -> List[UserInterface]:
        pass

    @abstractmethod
    async def getUsersAsync(self) -> List[UserInterface]:
        pass

    @abstractmethod
    async def removeUser(self, handle: str):
        pass

    @abstractmethod
    async def setUserEnabled(self, handle: str, enabled: bool):
        pass
