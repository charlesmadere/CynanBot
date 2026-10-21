from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Collection

from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


class TriviaGameControllersHelperInterface(ABC):

    class AbsAddResult(ABC):
        pass

    @dataclass(frozen = True, slots = True)
    class Added(AbsAddResult):
        newTotal: int
        userId: str
        userLogin: str
        userName: str

    @dataclass(frozen = True, slots = True)
    class AlreadyExists(AbsAddResult):
        pass

    @abstractmethod
    async def addChannelController(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> AbsAddResult:
        pass

    @abstractmethod
    async def addGlobalController(
        self,
        userId: str,
    ) -> AbsAddResult:
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
