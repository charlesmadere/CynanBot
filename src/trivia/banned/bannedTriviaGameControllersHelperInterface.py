from abc import ABC, abstractmethod
from typing import Collection

from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


class BannedTriviaGameControllersHelperInterface(ABC):

    @abstractmethod
    async def getBannedControllers(self) -> Collection[TwitchUserInterface]:
        pass
