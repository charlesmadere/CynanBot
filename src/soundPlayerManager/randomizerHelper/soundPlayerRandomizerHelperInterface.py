from abc import abstractmethod

from ..soundAlert import SoundAlert
from ...misc.clearable import Clearable


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
