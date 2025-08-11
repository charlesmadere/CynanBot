from abc import ABC, abstractmethod

from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore


class AnivCopyMessageTimeoutScoreRepositoryInterface(ABC):

    @abstractmethod
    async def getScore(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AnivCopyMessageTimeoutScore:
        pass

    @abstractmethod
    async def incrementDodgeScore(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AnivCopyMessageTimeoutScore:
        pass

    @abstractmethod
    async def incrementTimeoutScore(
        self,
        timeoutDurationSeconds: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AnivCopyMessageTimeoutScore:
        pass
