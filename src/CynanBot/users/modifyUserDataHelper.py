from datetime import datetime, timedelta, timezone
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.clearable import Clearable
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.users.modifyUserActionType import ModifyUserActionType
from CynanBot.users.modifyUserData import ModifyUserData
from CynanBot.users.modifyUserEventListener import ModifyUserEventListener


class ModifyUserDataHelper(Clearable):

    def __init__(
        self,
        timber: TimberInterface,
        timeToLive: timedelta = timedelta(minutes = 2, seconds = 30),
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(timeToLive, timedelta), f"malformed {timeToLive=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__timber: TimberInterface = timber
        self.__timeToLive: timedelta = timeToLive
        self.__timeZone: timezone = timeZone

        self.__modifyUserData: Optional[ModifyUserData] = None
        self.__modifyUserEventListener: Optional[ModifyUserEventListener] = None
        self.__setTime: Optional[datetime] = None

    async def clearCaches(self):
        self.__modifyUserData = None
        self.__setTime = None
        self.__timber.log('ModifyUserDataHelper', 'Caches cleared')

    async def getUserData(self) -> Optional[ModifyUserData]:
        now = datetime.now(self.__timeZone)

        if self.__setTime is None or self.__setTime + self.__timeToLive < now:
            self.__modifyUserData = None
            return None

        return self.__modifyUserData

    async def notifyModifyUserListenerAndClearData(self):
        modifyUserEventListener = self.__modifyUserEventListener
        if modifyUserEventListener is None:
            self.__timber.log('ModifyUserDataHelper', f'Attempted to notify listener of a user being modified, but no listener has been set')
            return

        modifyUserData = self.__modifyUserData
        if modifyUserData is None:
            self.__timber.log('ModifyUserDataHelper', f'Attempted to notify listener of a user being modified, but no user data has been set')
            return

        await self.clearCaches()
        await modifyUserEventListener.onModifyUserEvent(modifyUserData)

    def setModifyUserEventListener(self, listener: Optional[ModifyUserEventListener]):
        assert listener is None or isinstance(listener, ModifyUserEventListener), f"malformed {listener=}"

        self.__modifyUserEventListener = listener

    async def setUserData(
        self,
        actionType: ModifyUserActionType,
        userId: str,
        userName: str
    ):
        assert isinstance(actionType, ModifyUserActionType), f"malformed {actionType=}"
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__setTime = datetime.now(self.__timeZone)

        self.__modifyUserData = ModifyUserData(
            actionType = actionType,
            userId = userId,
            userName = userName
        )

        self.__timber.log('ModifyUserDataHelper', f'Persisted user data: (actionType=\"{actionType}\") (userId=\"{userId}\") (userName=\"{userName}\")')
