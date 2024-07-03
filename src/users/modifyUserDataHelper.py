from datetime import datetime, timedelta

from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc.clearable import Clearable
from ..timber.timberInterface import TimberInterface
from .modifyUserActionType import ModifyUserActionType
from .modifyUserData import ModifyUserData
from .modifyUserEventListener import ModifyUserEventListener
from ..misc import utils as utils


class ModifyUserDataHelper(Clearable):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        timeToLive: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(timeToLive, timedelta):
            raise TypeError(f'timeToLive argument is malformed: \"{timeToLive}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__timeToLive: timedelta = timeToLive

        self.__modifyUserData: ModifyUserData | None = None
        self.__modifyUserEventListener: ModifyUserEventListener | None = None
        self.__setTime: datetime | None = None

    async def clearCaches(self):
        self.__modifyUserData = None
        self.__setTime = None
        self.__timber.log('ModifyUserDataHelper', 'Caches cleared')

    async def getUserData(self) -> ModifyUserData | None:
        now = datetime.now(self.__timeZoneRepository.getDefault())

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

    def setModifyUserEventListener(self, listener: ModifyUserEventListener | None):
        if listener is not None and not isinstance(listener, ModifyUserEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__modifyUserEventListener = listener

    async def setUserData(
        self,
        actionType: ModifyUserActionType,
        userId: str,
        userName: str
    ):
        if not isinstance(actionType, ModifyUserActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__setTime = datetime.now(self.__timeZoneRepository.getDefault())

        self.__modifyUserData = ModifyUserData(
            actionType = actionType,
            userId = userId,
            userName = userName
        )

        self.__timber.log('ModifyUserDataHelper', f'Persisted user data: (actionType=\"{actionType}\") (userId=\"{userId}\") (userName=\"{userName}\")')
