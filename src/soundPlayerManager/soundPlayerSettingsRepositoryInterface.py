from abc import abstractmethod

from misc.clearable import Clearable
from soundPlayerManager.soundAlert import SoundAlert


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
