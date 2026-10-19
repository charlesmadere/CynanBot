from abc import ABC, abstractmethod
from typing import Collection

from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


class TriviaGameControllersHelperInterface(ABC):

    @abstractmethod
    async def getChannelControllers(
        self,
        twitchChannelId: str,
    ) -> Collection[TwitchUserInterface]:
        pass

    @abstractmethod
    async def getGlobalControllers(self) -> Collection[TwitchUserInterface]:
        pass
