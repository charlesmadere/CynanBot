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
