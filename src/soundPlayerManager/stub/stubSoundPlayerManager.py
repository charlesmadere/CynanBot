from typing import Collection

from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...chatBand.chatBandInstrument import ChatBandInstrument


class StubSoundPlayerManager(SoundPlayerManagerInterface):

    async def getCurrentPlaySessionId(self) -> str | None:
        # this method is intentionally empty
        return None

    async def isPlaying(self) -> bool:
        # this method is intentionally empty
        return False

    async def playChatBandInstrument(
        self,
        instrument: ChatBandInstrument,
        volume: int | None = None
    ) -> str | None:
        # this method is intentionally empty
        return None

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> str | None:
        # this method is intentionally empty
        return None

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> str | None:
        # this method is intentionally empty
        return None

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> str | None:
        # this method is intentionally empty
        return None

    async def stop(self) -> str | None:
        # this method is intentionally empty
        return None

    async def stopPlaySessionId(self, playSessionId: str | None) -> bool:
        # this method is intentionally empty
        return True
