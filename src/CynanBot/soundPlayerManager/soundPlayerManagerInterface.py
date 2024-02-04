from abc import ABC, abstractmethod

from CynanBot.soundPlayerHelper.soundAlert import SoundAlert


class SoundPlayerManagerInterface(ABC):

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playSoundAlert(self, alert: SoundAlert):
        pass
