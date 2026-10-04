from abc import ABC, abstractmethod
from datetime import datetime

from .models.preparedCutenessChampionsResult import PreparedCutenessChampionsResult
from .models.preparedCutenessHistoryResult import PreparedCutenessHistoryResult
from .models.preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry
from .models.preparedCutenessLeaderboardHistoryResult import PreparedCutenessLeaderboardHistoryResult
from .models.preparedCutenessLeaderboardResult import PreparedCutenessLeaderboardResult
from .models.preparedCutenessResult import PreparedCutenessResult


class CutenessPresenterInterface(ABC):

    @abstractmethod
    async def printCuteness(
        self,
        result: PreparedCutenessResult,
    ) -> str:
        pass

    @abstractmethod
    async def printCutenessChampions(
        self,
        result: PreparedCutenessChampionsResult,
        delimiter: str = ', ',
    ) -> str:
        pass

    @abstractmethod
    def printCutenessDate(self, dateTime: datetime) -> str:
        pass

    @abstractmethod
    def printCutenessHistory(
        self,
        result: PreparedCutenessHistoryResult,
        delimiter: str = ', ',
    ) -> str:
        pass

    @abstractmethod
    async def printLeaderboard(
        self,
        result: PreparedCutenessLeaderboardResult,
        delimiter: str = ', ',
    ) -> str:
        pass

    @abstractmethod
    async def printLeaderboardHistory(
        self,
        result: PreparedCutenessLeaderboardHistoryResult,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' — ',
    ) -> str:
        pass

    @abstractmethod
    def printLeaderboardPlacement(
        self,
        entry: PreparedCutenessLeaderboardEntry,
    ) -> str:
        pass
