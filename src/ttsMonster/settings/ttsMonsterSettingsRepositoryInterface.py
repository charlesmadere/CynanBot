from abc import ABC, abstractmethod

from ..models.ttsMonsterDonationPrefixConfig import TtsMonsterDonationPrefixConfig
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc.clearable import Clearable


class TtsMonsterSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getDefaultVoice(self) -> TtsMonsterVoice:
        pass

    @abstractmethod
    async def getDonationPrefixConfig(self) -> TtsMonsterDonationPrefixConfig:
        pass

    @abstractmethod
    async def getFileExtension(self) -> str:
        pass

    @abstractmethod
    async def getLoudVoiceMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def getLoudVoices(self) -> frozenset[TtsMonsterVoice]:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def useVoiceDependentMediaPlayerVolume(self) -> bool:
        pass
