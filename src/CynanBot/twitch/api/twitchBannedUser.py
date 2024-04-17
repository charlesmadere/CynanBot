from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class TwitchBannedUser():

    def __init__(
        self,
        createdAt: SimpleDateTime,
        expiresAt: SimpleDateTime | None,
        moderatorId: str,
        moderatorLogin: str,
        moderatorName: str,
        reason: str | None,
        userId: str,
        userLogin: str,
        userName: str
    ):
        if not isinstance(createdAt, SimpleDateTime):
            raise TypeError(f'createdAt argument is malformed: \"{createdAt}\"')
        elif expiresAt is not None and not isinstance(expiresAt, SimpleDateTime):
            raise TypeError(f'expiresAt argument is malformed: \"{expiresAt}\"')
        elif not utils.isValidStr(moderatorId):
            raise TypeError(f'moderatorId argument is malformed: \"{moderatorId}\"')
        elif not utils.isValidStr(moderatorLogin):
            raise TypeError(f'moderatorLogin argument is malformed: \"{moderatorLogin}\"')
        elif not utils.isValidStr(moderatorName):
            raise TypeError(f'moderatorName argument is malformed: \"{moderatorName}\"')
        elif reason is not None and not isinstance(reason, str):
            raise TypeError(f'reason argument is malformed: \"{reason}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__createdAt: SimpleDateTime = createdAt
        self.__expiresAt: SimpleDateTime | None = expiresAt
        self.__moderatorId: str = moderatorId
        self.__moderatorLogin: str = moderatorLogin
        self.__moderatorName: str = moderatorName
        self.__reason: str | None = reason
        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName

    def getCreatedAt(self) -> SimpleDateTime:
        return self.__createdAt

    def getExpiresAt(self) -> SimpleDateTime | None:
        return self.__expiresAt

    def getModeratorId(self) -> str:
        return self.__moderatorId

    def getModeratorLogin(self) -> str:
        return self.__moderatorLogin

    def getModeratorName(self) -> str:
        return self.__moderatorName

    def getReason(self) -> str | None:
        return self.__reason

    def getUserId(self) -> str:
        return self.__userId

    def getUserLogin(self) -> str:
        return self.__userLogin

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'createdAt': self.__createdAt,
            'expiresAt': self.__expiresAt,
            'moderatorId': self.__moderatorId,
            'moderatorLogin': self.__moderatorLogin,
            'moderatorName': self.__moderatorName,
            'reason': self.__reason,
            'userId': self.__userId,
            'userLogin': self.__userLogin,
            'userName': self.__userName
        }
