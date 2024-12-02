from abc import ABC, abstractmethod
from typing import Collection

from .soundAlert import SoundAlert
from ..chatBand.chatBandInstrument import ChatBandInstrument


class SoundPlayerManagerInterface(ABC):

    @abstractmethod
    async def getCurrentPlaySessionId(self) -> str | None:
        pass

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playChatBandInstrument(
        self,
        instrument: ChatBandInstrument,
        volume: int | None = None
    ) -> str | None:
        pass

    @abstractmethod
    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> str | None:
        pass

    @abstractmethod
    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> str | None:
        pass

    @abstractmethod
    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> str | None:
        pass

    @abstractmethod
    async def stop(self) -> str | None:
        pass

    @abstractmethod
    async def stopPlaySessionId(self, playSessionId: str | None) -> bool:
        pass
