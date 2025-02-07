from abc import abstractmethod

from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice
from ...misc.clearable import Clearable


class TtsMonsterSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getDefaultVoice(self) -> TtsMonsterWebsiteVoice:
        pass

    @abstractmethod
    async def getFileExtension(self) -> str:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def isWebsiteVoiceEnabled(self, websiteVoice: TtsMonsterWebsiteVoice) -> bool:
        pass

    @abstractmethod
    async def usePrivateApiFirst(self) -> bool:
        pass
