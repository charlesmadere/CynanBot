from abc import ABC, abstractmethod
from typing import Collection

from .twitchUserData import TwitchUserData
from ..localModels.twitchUserInterface import TwitchUserInterface
from ...misc.clearable import Clearable


class TwitchUserIdsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getById(
        self,
        userId: str,
    ) -> TwitchUserData | None:
        pass

    @abstractmethod
    async def getByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> TwitchUserData | None:
        pass

    @abstractmethod
    async def getIdByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> str | None:
        pass

    @abstractmethod
    async def requireById(
        self,
        userId: str,
    ) -> TwitchUserData:
        pass

    @abstractmethod
    async def requireByLoginOrName(
        self,
        userLoginOrName: str,
    ) -> TwitchUserData:
        pass

    @abstractmethod
    async def requireIdByLoginOrName(
        self,
        userLoginOrName: str,
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
