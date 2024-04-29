from abc import ABC, abstractmethod


class TimeoutImmuneUserIdsRepositoryInterface(ABC):

    @abstractmethod
    async def isImmune(self, userId: str) -> bool:
        pass
