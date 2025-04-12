from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class CheerActionSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getMaximumPerTwitchChannel(self) -> int:
        pass
