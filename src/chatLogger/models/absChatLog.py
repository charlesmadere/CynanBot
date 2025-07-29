from abc import ABC, abstractmethod

from ...misc.simpleDateTime import SimpleDateTime


class AbsChatLog(ABC):

    @abstractmethod
    def getDateTime(self) -> SimpleDateTime:
        pass

    @abstractmethod
    def getTwitchChannel(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass
