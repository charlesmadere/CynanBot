from abc import abstractmethod

from ..misc.clearable import Clearable


class UserIdsRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchAnonymousUserId(self) -> str:
        pass

    @abstractmethod
    async def fetchAnonymousUserName(self, twitchAccessToken: str) -> str | None:
        pass

    @abstractmethod
    async def fetchUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> str | None:
        pass

    @abstractmethod
    async def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> int | None:
        pass

    @abstractmethod
    async def fetchUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None
    ) -> str | None:
        pass

    @abstractmethod
    async def optionallySetUser(
        self,
        userId: str | None,
        userName: str | None
    ):
        pass

    @abstractmethod
    async def requireAnonymousUserId(self) -> str:
        pass

    @abstractmethod
    async def requireAnonymousUserName(self, twitchAccessToken: str) -> str:
        pass

    @abstractmethod
    async def requireUserId(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> str:
        pass

    @abstractmethod
    async def requireUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str | None = None
    ) -> int:
        pass

    @abstractmethod
    async def requireUserName(
        self,
        userId: str,
        twitchAccessToken: str | None = None
    ) -> str:
        pass

    @abstractmethod
    async def setUser(self, userId: str, userName: str):
        pass
