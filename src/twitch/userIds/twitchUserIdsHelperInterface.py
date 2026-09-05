from abc import ABC, abstractmethod
from typing import Collection

from .twitchUserData import TwitchUserData
from ..localModels.twitchUserInterface import TwitchUserInterface


class TwitchUserIdsHelperInterface(ABC):

    @abstractmethod
    async def getById(
        self,
        userId: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData | None:
        pass

    @abstractmethod
    async def getByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData | None:
        pass

    @abstractmethod
    async def getIdByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> str | None:
        pass

    @abstractmethod
    async def requireById(
        self,
        userId: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData:
        pass

    @abstractmethod
    async def requireByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> TwitchUserData:
        pass

    @abstractmethod
    async def requireIdByLoginOrName(
        self,
        userLoginOrName: str,
        twitchAccessToken: str | None = None,
    ) -> str:
        pass

    @abstractmethod
    async def set(
        self,
        userId: str,
        userLogin: str,
        userName: str,
    ):
        pass

    @abstractmethod
    async def setAll(
        self,
        users: Collection[TwitchUserInterface],
    ):
        pass
