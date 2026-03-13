from abc import ABC, abstractmethod

from ..models.preparedCutenessResult import PreparedCutenessResult


class CutenessHelperInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> PreparedCutenessResult:
        pass
