from abc import abstractmethod

from ..misc.clearable import Clearable


class CrowdControlSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getActionCooldownSeconds(self) -> float:
        pass

    @abstractmethod
    async def getMaxHandleAttempts(self) -> int:
        pass

    @abstractmethod
    async def getSecondsToLive(self) -> int:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
