from abc import ABC, abstractmethod

from ..models.absGoogleVoicePreset import AbsGoogleVoicePreset
from ..models.googleTtsFileReference import GoogleTtsFileReference


class GoogleTtsHelperInterface(ABC):

    @abstractmethod
    async def generateTts(
        self,
        voicePreset: AbsGoogleVoicePreset | None,
        allowMultiSpeaker: bool,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> GoogleTtsFileReference | None:
        pass
