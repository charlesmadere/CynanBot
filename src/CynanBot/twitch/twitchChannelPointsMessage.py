from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchConfigurationType import TwitchConfigurationType
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
            raise ValueError(f'eventId argument is malformed: \"{eventId}\"')
        elif redemptionMessage is not None and not isinstance(redemptionMessage, str):
            raise ValueError(f'redemptionMessage argument is malformed: \"{redemptionMessage}\"')
        elif not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

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
