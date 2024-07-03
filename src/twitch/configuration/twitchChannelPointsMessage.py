from twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from users.userInterface import UserInterface

from ..misc import utils as utils


class TwitchChannelPointsMessage():

    def __init__(
        self,
        eventId: str,
        redemptionMessage: str | None,
        rewardId: str,
        twitchUser: UserInterface,
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(eventId):
            raise TypeError(f'eventId argument is malformed: \"{eventId}\"')
        elif redemptionMessage is not None and not isinstance(redemptionMessage, str):
            raise TypeError(f'redemptionMessage argument is malformed: \"{redemptionMessage}\"')
        elif not utils.isValidStr(rewardId):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif not isinstance(twitchUser, UserInterface):
            raise TypeError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__eventId: str = eventId
        self.__redemptionMessage: str | None = redemptionMessage
        self.__rewardId: str = rewardId
        self.__twitchUser: UserInterface = twitchUser
        self.__userId: str = userId
        self.__userName: str = userName

    def getEventId(self) -> str:
        return self.__eventId

    def getRedemptionMessage(self) -> str | None:
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
