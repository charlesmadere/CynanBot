from abc import ABC, abstractmethod

from ..absTimeoutDuration import AbsTimeoutDuration
from ..timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ....users.userInterface import UserInterface


class AbsTimeoutAction(ABC):

    @abstractmethod
    def getActionId(self) -> str:
        pass

    @abstractmethod
    def getInstigatorUserId(self) -> str:
        pass

    @abstractmethod
    def getModeratorTwitchAccessToken(self) -> str:
        pass

    @abstractmethod
    def getModeratorUserId(self) -> str:
        pass

    @abstractmethod
    def getStreamStatusRequirement(self) -> TimeoutStreamStatusRequirement | None:
        pass

    @abstractmethod
    def getTimeoutDuration(self) -> AbsTimeoutDuration:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChatMessageId(self) -> str | None:
        pass

    @abstractmethod
    def getUser(self) -> UserInterface:
        pass

    @abstractmethod
    def getUserTwitchAccessToken(self) -> str:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.getUser().handle
