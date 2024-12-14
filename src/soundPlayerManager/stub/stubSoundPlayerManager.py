from typing import Collection

from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...chatBand.chatBandInstrument import ChatBandInstrument


class StubSoundPlayerManager(SoundPlayerManagerInterface):

    @property
    def isPlaying(self) -> bool:
        # this method is intentionally empty
        return False

    async def playChatBandInstrument(
        self,
        instrument: ChatBandInstrument,
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> bool:
        # this method is intentionally empty
        return False

    async def stop(self):
        # this method is intentionally empty
        pass
