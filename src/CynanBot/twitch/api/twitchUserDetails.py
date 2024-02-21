import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from CynanBot.twitch.api.twitchUserType import TwitchUserType


class TwitchUserDetails():

    def __init__(
        self,
        displayName: str,
        login: str,
        userId: str,
        broadcasterType: TwitchBroadcasterType,
        userType: TwitchUserType
    ):
        if not utils.isValidStr(displayName):
            raise ValueError(f'displayName argument is malformed: \"{displayName}\"')
        if not utils.isValidStr(login):
            raise ValueError(f'login argument is malformed: \"{login}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(broadcasterType, TwitchBroadcasterType), f"malformed {broadcasterType=}"
        assert isinstance(userType, TwitchUserType), f"malformed {userType=}"

        self.__displayName: str = displayName
        self.__login: str = login
        self.__userId: str = userId
        self.__broadcasterType: TwitchBroadcasterType = broadcasterType
        self.__userType: TwitchUserType = userType

    def getBroadcasterType(self) -> TwitchBroadcasterType:
        return self.__broadcasterType

    def getDisplayName(self) -> str:
        return self.__displayName

    def getLogin(self) -> str:
        return self.__login

    def getUserId(self) -> str:
        return self.__userId

    def getUserType(self) -> TwitchUserType:
        return self.__userType
