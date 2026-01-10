from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class UserIdsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None,
    ) -> str | None:
        pass

    @abstractmethod
    async def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None,
    ) -> int | None:
        pass

    @abstractmethod
    async def fetchUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None,
    ) -> str | None:
        pass

    @abstractmethod
    async def requireUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None,
    ) -> str:
        pass

    @abstractmethod
    async def requireUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None,
    ) -> int:
        pass

    @abstractmethod
    async def requireUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None,
    ) -> str:
        pass

    @abstractmethod
    async def setUser(self, userId: str, userName: str):
        pass

    @abstractmethod
    async def setUsers(self, userIdToUserName: dict[str, str]):
        pass
