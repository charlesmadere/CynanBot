from abc import ABC, abstractmethod

from ..models.commodoreSamFileReference import CommodoreSamFileReference


class CommodoreSamHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CommodoreSamFileReference | None:
        pass
