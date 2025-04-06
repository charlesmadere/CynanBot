from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TimeoutImmuneUserIdsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getOtherUserIds(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def getUserIds(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def isImmune(self, userId: str) -> bool:
        pass
