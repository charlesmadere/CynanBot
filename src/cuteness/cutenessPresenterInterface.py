from abc import ABC, abstractmethod

from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardResult import CutenessLeaderboardResult
from .cutenessResult import CutenessResult


class CutenessPresenterInterface(ABC):

    @abstractmethod
    async def printCuteness(self, result: CutenessResult) -> str:
        pass

    @abstractmethod
    async def printCutenessChampions(
        self,
        result: CutenessChampionsResult,
        delimiter: str = ', '
    ) -> str:
        pass

    @abstractmethod
    async def printLeaderboard(
        self,
        result: CutenessLeaderboardResult,
        delimiter: str = ', '
    ) -> str:
        pass

    @abstractmethod
    async def printLeaderboardPlacement(self, entry: CutenessLeaderboardEntry) -> str:
        pass
