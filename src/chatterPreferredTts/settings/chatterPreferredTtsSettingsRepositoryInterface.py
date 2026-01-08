from abc import ABC, abstractmethod

from ...misc.clearable import Clearable
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getEnabledTtsProviders(self) -> frozenset[TtsProvider]:
        pass

    @abstractmethod
    async def getHighTierTtsProviders(self) -> frozenset[TtsProvider]:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
