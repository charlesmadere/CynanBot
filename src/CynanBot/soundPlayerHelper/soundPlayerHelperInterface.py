from abc import ABC, abstractmethod

from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundReferenceInterface import \
    SoundReferenceInterface


class SoundPlayerHelperInterface(ABC):

    @abstractmethod
    async def loadSoundAlert(self, soundAlert: SoundAlert) -> SoundReferenceInterface:
        pass
