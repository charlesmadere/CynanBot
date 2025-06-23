from abc import ABC, abstractmethod

from ..models.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from ...misc.clearable import Clearable


class GoogleSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def getVoiceAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        pass

    @abstractmethod
    async def getVolumeGainDb(self) -> float | None:
        pass

    @abstractmethod
    async def isMultiSpeakerEnabled(self) -> bool:
        pass

    @abstractmethod
    async def useDonationPrefix(self) -> bool:
        pass
