from abc import abstractmethod
from typing import Optional

from CynanBot.misc.clearable import Clearable
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert


class SoundPlayerSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getSoundPathFor(self, soundAlert: SoundAlert) -> Optional[str]:
        pass
