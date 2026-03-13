from abc import ABC, abstractmethod

from ..models.cutenessResult import CutenessResult


class CutenessRepositoryInterface(ABC):

    @abstractmethod
    async def fetchCuteness(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> CutenessResult:
        pass
