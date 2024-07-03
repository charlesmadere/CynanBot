from abc import abstractmethod

from ..misc.clearable import Clearable


class AnivSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getCopyMessageMaxAgeSeconds(self) -> int:
        pass

    @abstractmethod
    async def getCopyMessageTimeoutProbability(self) -> float:
        pass

    @abstractmethod
    async def getCopyMessageTimeoutSeconds(self) -> int:
        pass
