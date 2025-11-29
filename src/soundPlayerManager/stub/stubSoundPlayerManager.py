from typing import Collection

from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerPlaylist import SoundPlayerPlaylist


class StubSoundPlayerManager(SoundPlayerManagerInterface):

    @property
    def isLoadingOrPlaying(self) -> bool:
        # this method is intentionally empty
        return False

    async def playPlaylist(
        self,
        playlist: SoundPlayerPlaylist,
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None,
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None,
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundFiles(
        self,
        filePaths: Collection[str],
        volume: int | None = None,
    ) -> bool:
        # this method is intentionally empty
        return False

    async def stop(self):
        # this method is intentionally empty
        pass
