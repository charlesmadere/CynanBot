from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


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
        assert isinstance(createdAt, SimpleDateTime), f"malformed {createdAt=}"
        assert expiresAt is None or isinstance(expiresAt, SimpleDateTime), f"malformed {expiresAt=}"
        if not utils.isValidStr(moderatorId):
            raise TypeError(f'moderatorId argument is malformed: \"{moderatorId}\"')
        if not utils.isValidStr(moderatorLogin):
            raise TypeError(f'moderatorLogin argument is malformed: \"{moderatorLogin}\"')
        if not utils.isValidStr(moderatorName):
            raise TypeError(f'moderatorName argument is malformed: \"{moderatorName}\"')
        assert reason is None or isinstance(reason, str), f"malformed {reason=}"
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        if not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

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
