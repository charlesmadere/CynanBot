from abc import ABC, abstractmethod

from ..models.cutenessChampionsResult import CutenessChampionsResult
from ..models.cutenessResult import CutenessResult


class CutenessRepositoryInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(
        self,
        twitchChannelId: str,
    ) -> CutenessChampionsResult:
        pass
