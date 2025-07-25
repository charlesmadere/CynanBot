from abc import ABC, abstractmethod


class AbsTimeoutActionData(ABC):

    @abstractmethod
    def getInstigatorUserId(self) -> str:
        pass

    @abstractmethod
    def getModeratorTwitchAccessToken(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannel(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChatMessageId(self) -> str | None:
        pass

    @abstractmethod
    def getUserTwitchAccessToken(self) -> str:
        pass
