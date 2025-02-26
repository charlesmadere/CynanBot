from abc import ABC, abstractmethod

from ...misc.clearable import Clearable
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass

    @abstractmethod
    async def isTtsProviderEnabled(self, provider: TtsProvider) -> bool:
        pass
