from abc import abstractmethod

from ...misc.clearable import Clearable


class MicrosoftSamSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass
