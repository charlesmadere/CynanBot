from abc import abstractmethod

from ...misc.clearable import Clearable


class GoogleSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass
