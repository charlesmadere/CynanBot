from abc import ABC, abstractmethod

from ..models.googleTtsFileReference import GoogleTtsFileReference
from ..models.googleVoicePreset import GoogleVoicePreset


class GoogleTtsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voicePreset: GoogleVoicePreset | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> GoogleTtsFileReference | None:
        pass
