from abc import ABC, abstractmethod

from frozendict import frozendict

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
    async def getVoiceVolumes(self) -> frozendict[TtsMonsterVoice, int | None]:
        pass
