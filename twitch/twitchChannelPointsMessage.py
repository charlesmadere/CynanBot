from typing import Optional

from twitch.twitchConfigurationType import TwitchConfigurationType
from users.user import User


class TwitchChannelPointsMessage():

    def getEventId(self) -> str:
        pass

    def getRedemptionMessage(self) -> Optional[str]:
        pass

    def getRewardId(self) -> str:
        pass

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    def getTwitchUser(self) -> User:
        pass

    def getUserId(self) -> str:
        pass

    def getUserName(self) -> str:
        pass
