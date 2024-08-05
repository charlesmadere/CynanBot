from abc import abstractmethod
from typing import Any, Collection

from .userInterface import UserInterface
from .userJsonConstant import UserJsonConstant
from ..misc.clearable import Clearable


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
    def getUsers(self) -> Collection[UserInterface]:
        pass

    @abstractmethod
    async def getUsersAsync(self) -> Collection[UserInterface]:
        pass

    @abstractmethod
    async def modifyUserValue(self, handle: str, jsonConstant: UserJsonConstant, value: Any | None):
        pass

    @abstractmethod
    async def removeUser(self, handle: str):
        pass

    @abstractmethod
    async def setUserEnabled(self, handle: str, enabled: bool):
        pass
