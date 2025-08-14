from abc import ABC, abstractmethod

from ..models.preparedChatterTimeoutHistory import PreparedChatterTimeoutHistory


class ChatterTimeoutHistoryHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedChatterTimeoutHistory:
        pass
