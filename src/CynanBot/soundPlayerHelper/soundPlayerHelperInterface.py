from abc import ABC, abstractmethod
from typing import Optional
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundReferenceInterface import SoundReferenceInterface


class SoundPlayerHelperInterface(ABC):

    @abstractmethod
    async def loadSoundAlert(self, soundAlert: SoundAlert) -> Optional[SoundReferenceInterface]:
        pass
