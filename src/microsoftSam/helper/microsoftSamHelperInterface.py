from abc import ABC, abstractmethod

from ..models.microsoftSamFileReference import MicrosoftSamFileReference
from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voice: MicrosoftSamVoice | None,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> MicrosoftSamFileReference | None:
        pass
