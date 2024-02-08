from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class SoundPlayerManagerInterface(ABC):

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playSoundAlert(self, alert: SoundAlert) -> bool:
        pass

    @abstractmethod
    async def playSoundFile(self, filePath: Optional[str]) -> bool:
        pass
