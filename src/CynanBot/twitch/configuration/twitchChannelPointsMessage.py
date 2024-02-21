from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.users.userInterface import UserInterface


class TwitchChannelPointsMessage():

    def __init__(
        self,
        eventId: str,
        redemptionMessage: Optional[str],
        rewardId: str,
        twitchUser: UserInterface,
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(eventId):
            raise TypeError(f'eventId argument is malformed: \"{eventId}\"')
        assert redemptionMessage is None or isinstance(redemptionMessage, str), f"malformed {redemptionMessage=}"
        if not utils.isValidStr(rewardId):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')
        assert isinstance(twitchUser, UserInterface), f"malformed {twitchUser=}"
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__eventId: str = eventId
        self.__redemptionMessage: Optional[str] = redemptionMessage
        self.__rewardId: str = rewardId
        self.__twitchUser: UserInterface = twitchUser
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

    def getTwitchUser(self) -> UserInterface:
        return self.__twitchUser

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
