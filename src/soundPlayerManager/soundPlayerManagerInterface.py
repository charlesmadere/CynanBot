from abc import ABC, abstractmethod
from typing import Collection

from .soundAlert import SoundAlert
from .soundPlayerPlaylist import SoundPlayerPlaylist


class SoundPlayerManagerInterface(ABC):

    @property
    @abstractmethod
    def isLoadingOrPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playPlaylist(
        self,
        playlist: SoundPlayerPlaylist
    ) -> bool:
        pass

    @abstractmethod
    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> bool:
        pass

    @abstractmethod
    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> bool:
        pass

    @abstractmethod
    async def playSoundFiles(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
        pass

    @abstractmethod
    async def stop(self):
        pass
