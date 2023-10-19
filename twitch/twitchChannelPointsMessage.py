from abc import ABC, abstractmethod
from typing import Optional

from twitch.twitchConfigurationType import TwitchConfigurationType
from users.user import User


class TwitchChannelPointsMessage(ABC):

    @abstractmethod
    def getEventId(self) -> str:
        pass

    @abstractmethod
    def getRedemptionMessage(self) -> Optional[str]:
        pass

    @abstractmethod
    def getRewardId(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    def getTwitchUser(self) -> User:
        pass

    @abstractmethod
    def getUserId(self) -> str:
        pass

    @abstractmethod
    def getUserName(self) -> str:
        pass


class TwitchChannelPointsMessageStub(TwitchChannelPointsMessage):

    def __init__(
        self,
        eventId: str,
        redemptionMessage: Optional[str],
        rewardId: str,
        twitchUser: User,
        userId: str,
        userName: str
    ):
        self.__eventId: str = eventId
        self.__redemptionMessage: Optional[str] = redemptionMessage
        self.__rewardId: str = rewardId
        self.__twitchUser: User = twitchUser
        self.__userId: str = userId
        self.__userName: str = userName

    def getEventId(self) -> str:
        return self.__eventId

    def getRedemptionMessage(self) -> Optional[str]:
        return self.__redemptionMessage

    def getRewardId(self) -> str:
        return self.__rewardId

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.STUB

    def getTwitchUser(self) -> User:
        return self.__twitchUser

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
