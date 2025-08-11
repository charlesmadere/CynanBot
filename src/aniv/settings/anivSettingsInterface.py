from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class AnivSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def areCopyMessageTimeoutsEnabled(self) -> bool:
        pass

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
