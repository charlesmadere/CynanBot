from abc import ABC, abstractmethod

from .anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore


class AnivCopyMessageTimeoutScoreRepositoryInterface(ABC):

    @abstractmethod
    async def getScore(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> AnivCopyMessageTimeoutScore | None:
        pass

    @abstractmethod
    async def incrementDodgeScore(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> AnivCopyMessageTimeoutScore:
        pass

    @abstractmethod
    async def incrementTimeoutScore(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> AnivCopyMessageTimeoutScore:
        pass
