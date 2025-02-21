from abc import ABC, abstractmethod

from ..models.microsoftSamFileReference import MicrosoftSamFileReference


class MicrosoftSamHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MicrosoftSamFileReference | None:
        pass

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> bytes | None:
        pass
