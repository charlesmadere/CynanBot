import CynanBot.misc.utils as utils
from typing import Dict, Any
from CynanBot.misc.simpleDateTime import SimpleDateTime


class TwitchFollower():

    def __init__(
        self,
        followedAt: SimpleDateTime,
        userId: str,
        userLogin: str,
        userName: str
    ):
        if not isinstance(followedAt, SimpleDateTime):
            raise TypeError(f'followedAt argument is malformed: \"{followedAt}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__followedAt: SimpleDateTime = followedAt
        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName

    def getFollowedAt(self) -> SimpleDateTime:
        return self.__followedAt

    def getUserId(self) -> str:
        return self.__userId

    def getUserLogin(self) -> str:
        return self.__userLogin

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'followedAt': self.__followedAt,
            'userId': self.__userId,
            'userLogin': self.__userLogin,
            'userName': self.__userName
        }
