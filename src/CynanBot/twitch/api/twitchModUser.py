from typing import Any, Dict

import CynanBot.misc.utils as utils


class TwitchModUser():

    def __init__(
        self,
        userId: str,
        userLogin: str,
        userName: str
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName

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
            'userId': self.__userId,
            'userLogin': self.__userLogin,
            'userName': self.__userName
        }
