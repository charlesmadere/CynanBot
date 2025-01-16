from abc import abstractmethod

from ..misc.clearable import Clearable


class CheerActionSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getMaximumPerTwitchChannel(self) -> int:
        pass
