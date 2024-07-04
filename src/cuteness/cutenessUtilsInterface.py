from abc import ABC, abstractmethod

from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessHistoryResult import CutenessHistoryResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult
from .cutenessResult import CutenessResult


class CutenessUtilsInterface(ABC):

    @abstractmethod
    def getCuteness(self, result: CutenessResult, delimiter: str) -> str:
        pass

    @abstractmethod
    def getCutenessChampions(self, result: CutenessChampionsResult, delimiter: str) -> str:
        pass

    @abstractmethod
    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        pass

    @abstractmethod
    def getCutenessLeaderboardHistory(
        self,
        result: CutenessLeaderboardHistoryResult,
        entryDelimiter: str,
        leaderboardDelimiter: str
    ) -> str:
        pass

    @abstractmethod
    def getLeaderboard(self, entries: list[CutenessLeaderboardEntry], delimiter: str) -> str:
        pass
