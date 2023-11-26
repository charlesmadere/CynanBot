from abc import abstractmethod
from typing import Optional

from CynanBot.misc.clearable import Clearable


class UserIdsRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchAnonymousUserId(self, twitchAccessToken: str) -> Optional[str]:
        pass

    @abstractmethod
    async def fetchAnonymousUserName(self, twitchAccessToken: str) -> Optional[str]:
        pass

    @abstractmethod
    async def fetchUserId(
        self,
        userName: str,
        twitchAccessToken: Optional[str] = None
    ) -> Optional[str]:
        pass

    @abstractmethod
    async def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: Optional[str] = None
    ) -> Optional[int]:
        pass

    @abstractmethod
    async def fetchUserName(
        self,
        userId: str,
        twitchAccessToken: Optional[str] = None
    ) -> Optional[str]:
        pass

    @abstractmethod
    async def requireAnonymousUserId(self, twitchAccessToken: str) -> str:
        pass

    @abstractmethod
    async def requireAnonymousUserName(self, twitchAccessToken: str) -> str:
        pass

    @abstractmethod
    async def requireUserId(
        self,
        userName: str,
        twitchAccessToken: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    async def requireUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: Optional[str] = None
    ) -> int:
        pass

    @abstractmethod
    async def requireUserName(
        self,
        userId: str,
        twitchAccessToken: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    async def setUser(self, userId: str, userName: str):
        pass
