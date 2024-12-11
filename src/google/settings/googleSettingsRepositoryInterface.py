from abc import abstractmethod

from ..models.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from ...misc.clearable import Clearable


class GoogleSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def getVoiceAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        pass
