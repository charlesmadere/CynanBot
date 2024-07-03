from abc import abstractmethod

from misc.clearable import Clearable
from soundPlayerManager.soundAlert import SoundAlert


class SoundPlayerRandomizerHelperInterface(Clearable):

    @abstractmethod
    async def chooseRandomFromDirectorySoundAlert(
        self,
        directoryPath: str | None
    ) -> str | None:
        pass

    @abstractmethod
    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        pass
