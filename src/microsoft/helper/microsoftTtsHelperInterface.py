from abc import ABC, abstractmethod

from ..models.microsoftTtsFileReference import MicrosoftTtsFileReference
from ..models.microsoftTtsVoice import MicrosoftTtsVoice


class MicrosoftTtsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voice: MicrosoftTtsVoice | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MicrosoftTtsFileReference | None:
        pass
