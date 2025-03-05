from abc import ABC, abstractmethod

from ..models.commodoreSamFileReference import CommodoreSamFileReference


class CommodoreSamHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CommodoreSamFileReference | None:
        pass
