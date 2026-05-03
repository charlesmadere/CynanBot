from abc import ABC, abstractmethod

from ..models.preparedCutenessChampionsResult import PreparedCutenessChampionsResult
from ..models.preparedCutenessResult import PreparedCutenessResult


class CutenessHelperInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedCutenessResult:
        pass

    @abstractmethod
    async def fetchCutenessChampions(
        self,
        twitchChannelId: str,
    ) -> PreparedCutenessChampionsResult:
        pass
