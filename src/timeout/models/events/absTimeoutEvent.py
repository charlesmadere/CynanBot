from abc import ABC, abstractmethod

from ..actions.absTimeoutAction import AbsTimeoutAction
from ....users.userInterface import UserInterface


class AbsTimeoutEvent(ABC):

    @abstractmethod
    def getEventId(self) -> str:
        pass

    @abstractmethod
    def getOriginatingAction(self) -> AbsTimeoutAction:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.getOriginatingAction().twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.getOriginatingAction().getTwitchChannelId()

    @property
    def twitchChatMessageId(self) -> str | None:
        return self.getOriginatingAction().getTwitchChatMessageId()

    @property
    def user(self) -> UserInterface:
        return self.getOriginatingAction().getUser()
