from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Collection

from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


class TriviaGameControllersHelperInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class AddedResult:
        newTotal: int
        userId: str
        userLogin: str
        userName: str

    @abstractmethod
    async def addBannedController(
        self,
        userId: str,
    ) -> AddedResult:
        pass

    @abstractmethod
    async def addChannelController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> AddedResult:
        pass

    @abstractmethod
    async def addGlobalController(
        self,
        userId: str,
    ) -> AddedResult:
        pass

    @abstractmethod
    async def getAllLocallyAuthorizedControllerIds(
        self,
        twitchChannelId: str,
    ) -> Collection[str]:
        pass

    @abstractmethod
    async def getBannedControllers(self) -> Collection[TwitchUserInterface]:
        pass

    @abstractmethod
    async def getChannelControllers(
        self,
        twitchChannelId: str,
    ) -> Collection[TwitchUserInterface]:
        pass

    @abstractmethod
    async def getGlobalControllers(self) -> Collection[TwitchUserInterface]:
        pass
