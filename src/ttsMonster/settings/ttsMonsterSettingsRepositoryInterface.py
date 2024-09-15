from abc import abstractmethod

from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice
from ...misc.clearable import Clearable


class TtsMonsterSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getDefaultVoice(self) -> TtsMonsterWebsiteVoice:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def isReturnCharacterUsageEnabled(self) -> bool:
        pass

    @abstractmethod
    async def isUsePrivateApiEnabled(self) -> bool:
        pass

    @abstractmethod
    async def isWebsiteVoiceEnabled(self, websiteVoice: TtsMonsterWebsiteVoice) -> bool:
        pass
