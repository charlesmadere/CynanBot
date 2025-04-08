from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class AnivSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getCopyMessageMaxAgeSeconds(self) -> int:
        pass

    @abstractmethod
    async def getCopyMessageTimeoutProbability(self) -> float:
        pass

    @abstractmethod
    async def getCopyMessageTimeoutSeconds(self) -> int:
        pass

    @abstractmethod
    async def getCopyMessageTimeoutMaxSeconds(self) -> int:
        pass

    @abstractmethod
    async def isRandomTimeoutScalingEnabled(self) -> bool:
        pass
