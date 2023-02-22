from datetime import datetime, timedelta, timezone
from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from users.modifyUserActionType import ModifyUserActionType
from users.modifyUserData import ModifyUserData
from users.modifyUserEventListener import ModifyUserEventListener


class ModifyUserDataHelper():

    def __init__(
        self,
        timber: Timber,
        timeToLive: timedelta = timedelta(minutes = 2, seconds = 30),
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeToLive, timedelta):
            raise ValueError(f'timeToLive argument is malformed: \"{timeToLive}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: Timber = timber
        self.__timeToLive: timedelta = timeToLive
        self.__timeZone: timezone = timeZone

        self.__modifyUserData: Optional[ModifyUserData] = None
        self.__modifyUserEventListener: Optional[ModifyUserEventListener] = None
        self.__setTime: Optional[datetime] = None

    async def clearCaches(self):
        self.__modifyUserData = None
        self.__setTime = None

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
        if listener is not None and not isinstance(listener, ModifyUserEventListener):
            raise ValueError(f'listener argument is malformed: \"{listener}\"')

        self.__modifyUserEventListener = listener

    async def setUserData(
        self,
        actionType: ModifyUserActionType,
        userId: str,
        userName: str
    ):
        if not isinstance(actionType, ModifyUserActionType):
            raise ValueError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__setTime = datetime.now(self.__timeZone)

        self.__modifyUserData = ModifyUserData(
            actionType = actionType,
            userId = userId,
            userName = userName
        )

        self.__timber.log('ModifyUserDataHelper', f'Persisted user data: (actionType=\"{actionType}\") (userId=\"{userId}\") (userName=\"{userName}\")')
