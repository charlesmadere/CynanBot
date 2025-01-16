from abc import ABC, abstractmethod


class TimeoutImmuneUserIdsRepositoryInterface(ABC):

    @abstractmethod
    async def getUserIds(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def isImmune(self, userId: str) -> bool:
        pass
