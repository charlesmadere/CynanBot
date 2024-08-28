from abc import abstractmethod

from ...misc.clearable import Clearable


class TimeoutCheerActionSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getBullyTimeToLiveDays(self) -> int:
        pass

    @abstractmethod
    async def getFailureProbability(self) -> float:
        pass

    @abstractmethod
    async def getReverseProbability(self) -> float:
        pass
