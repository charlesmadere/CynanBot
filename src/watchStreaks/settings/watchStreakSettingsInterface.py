from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class WatchStreakSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getMinimumWatchStreakForTts(self) -> int:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
