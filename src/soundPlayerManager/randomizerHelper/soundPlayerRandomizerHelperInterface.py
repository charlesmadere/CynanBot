from abc import ABC, abstractmethod

from ..soundAlert import SoundAlert
from ...misc.clearable import Clearable


class SoundPlayerRandomizerHelperInterface(Clearable, ABC):

    @abstractmethod
    async def chooseRandomFromDirectorySoundAlert(
        self,
        directoryPath: str | None,
    ) -> str | None:
        pass

    @abstractmethod
    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        pass
