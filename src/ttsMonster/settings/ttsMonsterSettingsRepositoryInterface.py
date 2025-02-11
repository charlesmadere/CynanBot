from abc import abstractmethod

from ...misc.clearable import Clearable


class TtsMonsterSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getFileExtension(self) -> str:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass
