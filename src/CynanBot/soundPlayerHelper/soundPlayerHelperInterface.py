from abc import ABC, abstractmethod

from CynanBot.soundPlayerHelper.soundAlert import SoundAlert


class SoundPlayerHelperInterface(ABC):

    @abstractmethod
    async def playSoundAlert(self, soundAlert: SoundAlert):
        pass
