from abc import ABC, abstractmethod

from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class ImmediateSoundPlayerManagerInterface(ABC):

    @abstractmethod
    async def playSoundAlert(self, alert: SoundAlert) -> bool:
        pass

    @abstractmethod
    async def playSoundFile(self, filePath: str |  None) -> bool:
        pass
