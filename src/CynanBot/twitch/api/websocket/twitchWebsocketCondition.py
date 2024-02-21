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
        assert broadcasterUserId is None or isinstance(broadcasterUserId, str), f"malformed {broadcasterUserId=}"
        assert broadcasterUserLogin is None or isinstance(broadcasterUserLogin, str), f"malformed {broadcasterUserLogin=}"
        assert broadcasterUserName is None or isinstance(broadcasterUserName, str), f"malformed {broadcasterUserName=}"
        assert clientId is None or isinstance(clientId, str), f"malformed {clientId=}"
        assert fromBroadcasterUserId is None or isinstance(fromBroadcasterUserId, str), f"malformed {fromBroadcasterUserId=}"
        assert fromBroadcasterUserLogin is None or isinstance(fromBroadcasterUserLogin, str), f"malformed {fromBroadcasterUserLogin=}"
        assert fromBroadcasterUserName is None or isinstance(fromBroadcasterUserName, str), f"malformed {fromBroadcasterUserName=}"
        assert moderatorUserId is None or isinstance(moderatorUserId, str), f"malformed {moderatorUserId=}"
        assert moderatorUserLogin is None or isinstance(moderatorUserLogin, str), f"malformed {moderatorUserLogin=}"
        assert moderatorUserName is None or isinstance(moderatorUserName, str), f"malformed {moderatorUserName=}"
        assert rewardId is None or isinstance(rewardId, str), f"malformed {rewardId=}"
        assert toBroadcasterUserId is None or isinstance(toBroadcasterUserId, str), f"malformed {toBroadcasterUserId=}"
        assert toBroadcasterUserLogin is None or isinstance(toBroadcasterUserLogin, str), f"malformed {toBroadcasterUserLogin=}"
        assert toBroadcasterUserName is None or isinstance(toBroadcasterUserName, str), f"malformed {toBroadcasterUserName=}"
        assert userId is None or isinstance(userId, str), f"malformed {userId=}"
        assert userLogin is None or isinstance(userLogin, str), f"malformed {userLogin=}"
        assert userName is None or isinstance(userName, str), f"malformed {userName=}"

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
