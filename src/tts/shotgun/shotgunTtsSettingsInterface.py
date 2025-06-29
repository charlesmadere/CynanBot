from abc import ABC, abstractmethod

from ..models.ttsProvider import TtsProvider
from ...misc.clearable import Clearable


class ShotgunTtsSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getEnabledTtsProviders(self) -> frozenset[TtsProvider]:
        pass

    @abstractmethod
    async def getProviderCount(self) -> int | None:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
