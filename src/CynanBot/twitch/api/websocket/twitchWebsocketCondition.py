from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils


class TwitchWebsocketCondition():

    def __init__(
        self,
        broadcasterUserId: Optional[str] = None,
        broadcasterUserLogin: Optional[str] = None,
        broadcasterUserName: Optional[str] = None,
        clientId: Optional[str] = None,
        fromBroadcasterUserId: Optional[str] = None,
        fromBroadcasterUserLogin: Optional[str] = None,
        fromBroadcasterUserName: Optional[str] = None,
        moderatorUserId: Optional[str] = None,
        moderatorUserLogin: Optional[str] = None,
        moderatorUserName: Optional[str] = None,
        rewardId: Optional[str] = None,
        toBroadcasterUserId: Optional[str] = None,
        toBroadcasterUserLogin: Optional[str] = None,
        toBroadcasterUserName: Optional[str] = None,
        userId: Optional[str] = None,
        userLogin: Optional[str] = None,
        userName: Optional[str] = None
    ):
        if broadcasterUserId is not None and not isinstance(broadcasterUserId, str):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif broadcasterUserLogin is not None and not isinstance(broadcasterUserLogin, str):
            raise TypeError(f'broadcasterUserLogin argument is malformed: \"{broadcasterUserLogin}\"')
        elif broadcasterUserName is not None and not isinstance(broadcasterUserName, str):
            raise TypeError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')
        elif clientId is not None and not isinstance(clientId, str):
            raise TypeError(f'clientId argument is malformed: \"{clientId}\"')
        elif fromBroadcasterUserId is not None and not isinstance(fromBroadcasterUserId, str):
            raise TypeError(f'fromBroadcasterUserId argument is malformed: \"{fromBroadcasterUserId}\"')
        elif fromBroadcasterUserLogin is not None and not isinstance(fromBroadcasterUserLogin, str):
            raise TypeError(f'fromBroadcasterUserLogin argument is malformed: \"{fromBroadcasterUserLogin}\"')
        elif fromBroadcasterUserName is not None and not isinstance(fromBroadcasterUserName, str):
            raise TypeError(f'fromBroadcasterUserName argument is malformed: \"{fromBroadcasterUserName}\"')
        elif moderatorUserId is not None and not isinstance(moderatorUserId, str):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif moderatorUserLogin is not None and not isinstance(moderatorUserLogin, str):
            raise TypeError(f'moderatorUserLogin argument is malformed: \"{moderatorUserLogin}\"')
        elif moderatorUserName is not None and not isinstance(moderatorUserName, str):
            raise TypeError(f'moderatorUserName argument is malformed: \"{moderatorUserName}\"')
        elif rewardId is not None and not isinstance(rewardId, str):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')
        elif toBroadcasterUserId is not None and not isinstance(toBroadcasterUserId, str):
            raise TypeError(f'toBroadcasterUserId argument is malformed: \"{toBroadcasterUserId}\"')
        elif toBroadcasterUserLogin is not None and not isinstance(toBroadcasterUserLogin, str):
            raise TypeError(f'toBroadcasterUserLogin argument is malformed: \"{toBroadcasterUserLogin}\"')
        elif toBroadcasterUserName is not None and not isinstance(toBroadcasterUserName, str):
            raise TypeError(f'toBroadcasterUserName argument is malformed: \"{toBroadcasterUserName}\"')
        elif userId is not None and not isinstance(userId, str):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif userLogin is not None and not isinstance(userLogin, str):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif userName is not None and not isinstance(userName, str):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__broadcasterUserId: Optional[str] = broadcasterUserId
        self.__broadcasterUserLogin: Optional[str] = broadcasterUserLogin
        self.__broadcasterUserName: Optional[str] = broadcasterUserName
        self.__clientId: Optional[str] = clientId
        self.__fromBroadcasterUserId: Optional[str] = fromBroadcasterUserId
        self.__fromBroadcasterUserLogin: Optional[str] = fromBroadcasterUserLogin
        self.__fromBroadcasterUserName: Optional[str] = fromBroadcasterUserName
        self.__moderatorUserId: Optional[str] = moderatorUserId
        self.__moderatorUserLogin: Optional[str] = moderatorUserLogin
        self.__moderatorUserName: Optional[str] = moderatorUserName
        self.__rewardId: Optional[str] = rewardId
        self.__toBroadcasterUserId: Optional[str] = toBroadcasterUserId
        self.__toBroadcasterUserLogin: Optional[str] = toBroadcasterUserLogin
        self.__toBroadcasterUserName: Optional[str] = toBroadcasterUserName
        self.__userId: Optional[str] = userId
        self.__userLogin: Optional[str] = userLogin
        self.__userName: Optional[str] = userName

    def getBroadcasterUserId(self) -> Optional[str]:
        return self.__broadcasterUserId

    def getBroadcasterUserLogin(self) -> Optional[str]:
        return self.__broadcasterUserLogin

    def getBroadcasterUserName(self) -> Optional[str]:
        return self.__broadcasterUserName

    def getClientId(self) -> Optional[str]:
        return self.__clientId

    def getFromBroadcasterUserId(self) -> Optional[str]:
        return self.__fromBroadcasterUserId

    def getFromBroadcasterUserLogin(self) -> Optional[str]:
        return self.__fromBroadcasterUserLogin

    def getFromBroadcasterUserName(self) -> Optional[str]:
        return self.__fromBroadcasterUserName

    def getModeratorUserId(self) -> Optional[str]:
        return self.__moderatorUserId

    def getModeratorUserLogin(self) -> Optional[str]:
        return self.__moderatorUserLogin

    def getModeratorUserName(self) -> Optional[str]:
        return self.__moderatorUserName

    def getRewardId(self) -> Optional[str]:
        return self.__rewardId

    def getToBroadcasterUserId(self) -> Optional[str]:
        return self.__toBroadcasterUserId

    def getToBroadcasterUserLogin(self) -> Optional[str]:
        return self.__toBroadcasterUserLogin

    def getToBroadcasterUserName(self) -> Optional[str]:
        return self.__toBroadcasterUserName

    def getUserId(self) -> Optional[str]:
        return self.__userId

    def getUserLogin(self) -> Optional[str]:
        return self.__userLogin

    def getUserName(self) -> Optional[str]:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireBroadcasterUserId(self) -> str:
        broadcasterUserId = self.__broadcasterUserId

        if not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId has not been set: \"{broadcasterUserId}\"')

        return broadcasterUserId

    def requireClientId(self) -> str:
        clientId = self.__clientId

        if not utils.isValidStr(clientId):
            raise ValueError(f'clientId has not been set: \"{clientId}\"')

        return clientId

    def requireFromBroadcasterUserId(self) -> str:
        fromBroadcasterUserId = self.__fromBroadcasterUserId

        if not utils.isValidStr(fromBroadcasterUserId):
            raise ValueError(f'fromBroadcasterUserId has not been set: \"{fromBroadcasterUserId}\"')

        return fromBroadcasterUserId

    def requireModeratorUserId(self) -> str:
        moderatorUserId = self.__moderatorUserId

        if not utils.isValidStr(moderatorUserId):
            raise ValueError(f'moderatorUserId has not been set: \"{moderatorUserId}\"')

        return moderatorUserId

    def requireRewardId(self) -> str:
        rewardId = self.__rewardId

        if not utils.isValidStr(rewardId):
            raise ValueError(f'rewardId has not been set: \"{rewardId}\"')

        return rewardId

    def requireToBroadcasterUserId(self) -> str:
        toBroadcasterUserId = self.__toBroadcasterUserId

        if not utils.isValidStr(toBroadcasterUserId):
            raise ValueError(f'toBroadcasterUserId has not been set: \"{toBroadcasterUserId}\"')

        return toBroadcasterUserId

    def requireUserId(self) -> str:
        userId = self.__userId

        if not utils.isValidStr(userId):
            raise ValueError(f'userId has not been set: \"{userId}\"')

        return userId

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'broadcasterUserId': self.__broadcasterUserId,
            'broadcasterUserLogin': self.__broadcasterUserLogin,
            'broadcasterUserName': self.__broadcasterUserName,
            'clientId': self.__clientId,
            'fromBroadcasterUserId': self.__fromBroadcasterUserId,
            'fromBroadcasterUserLogin': self.__fromBroadcasterUserLogin,
            'fromBroadcasterUserName': self.__fromBroadcasterUserName,
            'moderatorUserId': self.__moderatorUserId,
            'moderatorUserLogin': self.__moderatorUserLogin,
            'moderatorUserName': self.__moderatorUserName,
            'rewardId': self.__rewardId,
            'toBroadcasterUserId': self.__toBroadcasterUserId,
            'toBroadcasterUserLogin': self.__toBroadcasterUserLogin,
            'toBroadcasterUserName': self.__toBroadcasterUserName,
            'userId': self.__userId,
            'userLogin': self.__userLogin,
            'userName': self.__userName
        }
