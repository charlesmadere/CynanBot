from abc import abstractmethod

from ..misc.clearable import Clearable


class TimeoutActionSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getActionLoopCooldownSeconds(self) -> float:
        pass

    @abstractmethod
    async def getBullyTimeToLiveDays(self) -> int:
        pass

    @abstractmethod
    async def getDieSize(self) -> int:
        pass

    @abstractmethod
    async def getFailureProbability(self) -> float:
        pass

    @abstractmethod
    async def getGrenadeAdditionalReverseProbability(self) -> float:
        pass

    @abstractmethod
    async def getMaxBullyFailureOccurrences(self) -> int:
        pass

    @abstractmethod
    async def getMaxBullyFailureProbability(self) -> float:
        pass

    @abstractmethod
    async def getReverseProbability(self) -> float:
        pass
