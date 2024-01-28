from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class StreamAlertsSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getAlertsDelayBetweenSeconds(self) -> float:
        pass
