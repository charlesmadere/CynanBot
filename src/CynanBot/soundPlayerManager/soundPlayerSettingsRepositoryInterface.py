from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class SoundPlayerSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getFilePathFor(self, soundAlert: SoundAlert) -> str | None:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
