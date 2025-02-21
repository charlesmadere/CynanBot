from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class StreamAlertsSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getAlertsDelayBetweenSeconds(self) -> float:
        pass
