from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.simpleDateTime import SimpleDateTime


class TwitchBannedUser():

    def __init__(
        self,
        createdAt: SimpleDateTime,
        expiresAt: Optional[SimpleDateTime],
        moderatorId: str,
        moderatorLogin: str,
        moderatorName: str,
        reason: Optional[str],
        userId: str,
        userLogin: str,
        userName: str
    ):
        if not isinstance(createdAt, SimpleDateTime):
            raise ValueError(f'createdAt argument is malformed: \"{createdAt}\"')
        elif expiresAt is not None and not isinstance(expiresAt, SimpleDateTime):
            raise ValueError(f'expiresAt argument is malformed: \"{expiresAt}\"')
        elif not utils.isValidStr(moderatorId):
            raise ValueError(f'moderatorId argument is malformed: \"{moderatorId}\"')
        elif not utils.isValidStr(moderatorLogin):
            raise ValueError(f'moderatorLogin argument is malformed: \"{moderatorLogin}\"')
        elif not utils.isValidStr(moderatorName):
            raise ValueError(f'moderatorName argument is malformed: \"{moderatorName}\"')
        elif reason is not None and not isinstance(reason, str):
            raise ValueError(f'reason argument is malformed: \"{reason}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise ValueError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__createdAt: SimpleDateTime = createdAt
        self.__expiresAt: Optional[SimpleDateTime] = expiresAt
        self.__moderatorId: str = moderatorId
        self.__moderatorLogin: str = moderatorLogin
        self.__moderatorName: str = moderatorName
        self.__reason: Optional[str] = reason
        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName

    def getCreatedAt(self) -> SimpleDateTime:
        return self.__createdAt

    def getExpiresAt(self) -> Optional[SimpleDateTime]:
        return self.__expiresAt

    def getModeratorId(self) -> str:
        return self.__moderatorId

    def getModeratorLogin(self) -> str:
        return self.__moderatorLogin

    def getModeratorName(self) -> str:
        return self.__moderatorName

    def getReason(self) -> Optional[str]:
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

    def toDictionary(self) -> Dict[str, Any]:
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
