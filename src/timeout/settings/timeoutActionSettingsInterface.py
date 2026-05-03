from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TimeoutActionSettingsInterface(Clearable, ABC):

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
    async def getReverseProbability(self) -> float:
        pass

    @abstractmethod
    async def getTm36SplashDamageProbability(self) -> float:
        pass
