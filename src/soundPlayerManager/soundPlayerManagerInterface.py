from abc import ABC, abstractmethod

from .soundAlert import SoundAlert


class SoundPlayerManagerInterface(ABC):

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playSoundAlert(self, alert: SoundAlert) -> bool:
        pass

    @abstractmethod
    async def playSoundFile(self, filePath: str | None) -> bool:
        pass
