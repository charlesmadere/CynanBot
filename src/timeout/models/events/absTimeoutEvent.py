from abc import ABC, abstractmethod

from ..actions.absTimeoutAction import AbsTimeoutAction


class AbsTimeoutEvent(ABC):

    @abstractmethod
    def getEventId(self) -> str:
        pass

    @abstractmethod
    def getOriginatingAction(self) -> AbsTimeoutAction:
        pass

    def getTwitchChannelId(self) -> str:
        return self.getOriginatingAction().getTwitchChannelId()

    @property
    def twitchChannel(self) -> str:
        return self.getOriginatingAction().twitchChannel
