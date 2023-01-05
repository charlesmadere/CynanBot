from datetime import datetime, timedelta, timezone
from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from users.addUserData import AddUserData
from users.addUserEventListener import AddUserEventListener


class AddUserDataHelper():

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

        self.__addUserData: Optional[AddUserData] = None
        self.__addUserEventListener: Optional[AddUserEventListener] = None
        self.__setTime: Optional[datetime] = None

    async def clearUserData(self):
        self.__setTime = None
        self.__addUserData = None

    async def getUserData(self) -> Optional[AddUserData]:
        now = datetime(self.__timeZone)

        if self.__setTime is None or self.__setTime + self.__timeToLive < now:
            self.__addUserData = None
            return None

        return self.__addUserData

    async def notifyAddUserListenerAndClearData(self):
        addUserEventListener = self.__addUserEventListener
        if addUserEventListener is None:
            self.__timber.log('AddUserDataHelper', f'Attempted to notify listener of a new user being added, but no listener has been set')
            return

        addUserData = self.__addUserData
        if addUserData is None:
            self.__timber.log('AddUserDataHelper', f'Attempted to notify listener of a new user being added, but no user data has been set')
            return

        await self.clearUserData()
        await self.__addUserEventListener.onAddNewUserEvent(addUserData)

    def setAddUserEventListener(self, listener: Optional[AddUserEventListener]):
        self.__addUserEventListener = listener

    async def setUserData(
        self,
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__setTime = datetime(self.__timeZone)

        self.__addUserData = AddUserData(
            userId = userId,
            userName = userName
        )

        self.__timber.log('AddUserDataHelper', f'Persisted user data: (userId=\"{userId}\") (userName=\"{userName}\")')
