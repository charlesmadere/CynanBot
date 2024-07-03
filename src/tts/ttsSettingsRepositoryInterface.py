from abc import abstractmethod

from ..google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from ..misc.clearable import Clearable


class TtsSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getGoogleVoiceAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        pass

    @abstractmethod
    async def getGoogleVolumeGainDb(self) -> float | None:
        pass

    @abstractmethod
    async def getMaximumMessageSize(self) -> int:
        pass

    @abstractmethod
    async def getTtsDelayBetweenSeconds(self) -> float:
        pass

    @abstractmethod
    async def getTtsTimeoutSeconds(self) -> float:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass

    @abstractmethod
    async def requireDecTalkPath(self) -> str:
        pass
