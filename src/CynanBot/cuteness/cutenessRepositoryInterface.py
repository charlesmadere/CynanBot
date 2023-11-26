from abc import ABC, abstractmethod
from typing import Optional

from cuteness.cutenessChampionsResult import CutenessChampionsResult
from cuteness.cutenessHistoryResult import CutenessHistoryResult
from cuteness.cutenessLeaderboardHistoryResult import \
    CutenessLeaderboardHistoryResult
from cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult
from cuteness.cutenessResult import CutenessResult


class CutenessRepositoryInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        twitchChannel: str,
        userId: str,
        userName: str,
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(self, twitchChannel: str) -> CutenessChampionsResult:
        pass

    @abstractmethod
    async def fetchCutenessHistory(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessHistoryResult:
        pass

    @abstractmethod
    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboard(
        self,
        twitchChannel: str,
        specificLookupUserId: Optional[str] = None,
        specificLookupUserName: Optional[str] = None
    ) -> CutenessLeaderboardResult:
        pass

    @abstractmethod
    async def fetchCutenessLeaderboardHistory(self, twitchChannel: str) -> CutenessLeaderboardHistoryResult:
        pass
