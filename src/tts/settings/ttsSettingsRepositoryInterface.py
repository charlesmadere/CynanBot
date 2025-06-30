from abc import ABC, abstractmethod

from ..models.shotgun.shotgunProviderUseParameters import ShotgunProviderUseParameters
from ..models.ttsProvider import TtsProvider
from ...misc.clearable import Clearable


class TtsSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getRandoEnabledProviders(self) -> frozenset[TtsProvider]:
        pass

    @abstractmethod
    async def getShotgunEnabledProviders(self) -> frozenset[TtsProvider]:
        pass

    @abstractmethod
    async def getShotgunProviderUseParameters(self) -> ShotgunProviderUseParameters:
        pass

    @abstractmethod
    async def getMaximumMessageSize(self) -> int:
        pass

    @abstractmethod
    async def getTtsTimeoutSeconds(self) -> float:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
