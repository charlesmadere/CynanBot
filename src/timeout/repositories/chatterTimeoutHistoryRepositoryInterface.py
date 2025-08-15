from abc import ABC, abstractmethod

from ..models.chatterTimeoutHistory import ChatterTimeoutHistory
from ...misc.clearable import Clearable


class ChatterTimeoutHistoryRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def add(
        self,
        durationSeconds: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterTimeoutHistory:
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterTimeoutHistory:
        pass
