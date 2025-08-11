from abc import ABC, abstractmethod

from ..models.preparedAnivCopyMessageTimeoutScore import PreparedAnivCopyMessageTimeoutScore


class AnivCopyMessageTimeoutScoreHelperInterface(ABC):

    @abstractmethod
    async def getScore(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedAnivCopyMessageTimeoutScore:
        pass
