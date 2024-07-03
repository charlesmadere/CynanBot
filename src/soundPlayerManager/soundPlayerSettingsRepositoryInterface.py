from abc import abstractmethod

from .soundAlert import SoundAlert
from ..misc.clearable import Clearable


class SoundPlayerSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def areShiniesEnabled(self) -> bool:
        pass

    @abstractmethod
    async def getFilePathFor(self, soundAlert: SoundAlert) -> str | None:
        pass

    @abstractmethod
    async def getShinyProbability(self) -> float:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
