from abc import ABC, abstractmethod

from ..models.googleTtsFileReference import GoogleTtsFileReference


class GoogleTtsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> GoogleTtsFileReference | None:
        pass
