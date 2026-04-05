from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class CutenessSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getHistorySize(self) -> int:
        pass

    @abstractmethod
    async def getLeaderboardSize(self) -> int:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
