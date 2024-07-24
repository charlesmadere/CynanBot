from datetime import datetime, timedelta

from .addOrRemoveUserActionType import AddOrRemoveUserActionType
from .addOrRemoveUserData import AddOrRemoveUserData
from .addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from .addOrRemoveUserEventListener import AddOrRemoveUserEventListener
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class AddOrRemoveUserDataHelper(AddOrRemoveUserDataHelperInterface):

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

        self.__addOrRemoveUserData: AddOrRemoveUserData | None = None
        self.__addOrRemoveUserEventListener: AddOrRemoveUserEventListener | None = None
        self.__setTime: datetime | None = None

    async def clearCaches(self):
        self.__addOrRemoveUserData = None
        self.__setTime = None
        self.__timber.log('AddOrRemoveUserDataHelper', 'Caches cleared')

    async def getData(self) -> AddOrRemoveUserData | None:
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if self.__setTime is None or self.__setTime + self.__timeToLive < now:
            self.__addOrRemoveUserData = None
            return None

        return self.__addOrRemoveUserData

    async def notifyAddOrRemoveUserEventListenerAndClearData(self):
        addOrRemoveUserEventListener = self.__addOrRemoveUserEventListener
        if addOrRemoveUserEventListener is None:
            self.__timber.log('AddOrRemoveUserDataHelper', f'Attempted to notify listener of a user being modified, but no listener has been set')
            return

        addOrRemoveUserData = self.__addOrRemoveUserData
        if addOrRemoveUserData is None:
            self.__timber.log('AddOrRemoveUserDataHelper', f'Attempted to notify listener of a user being modified, but no user data has been set')
            return

        await self.clearCaches()
        await addOrRemoveUserEventListener.onAddOrRemoveUserEvent(addOrRemoveUserData)

    def setAddOrRemoveUserEventListener(self, listener: AddOrRemoveUserEventListener | None):
        if listener is not None and not isinstance(listener, AddOrRemoveUserEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__addOrRemoveUserEventListener = listener

    async def setUserData(
        self,
        actionType: AddOrRemoveUserActionType,
        userId: str,
        userName: str
    ):
        if not isinstance(actionType, AddOrRemoveUserActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__setTime = datetime.now(self.__timeZoneRepository.getDefault())

        self.__addOrRemoveUserData = AddOrRemoveUserData(
            actionType = actionType,
            userId = userId,
            userName = userName
        )

        self.__timber.log('AddOrRemoveUserDataHelper', f'Persisted user data: (actionType=\"{actionType}\") (userId=\"{userId}\") (userName=\"{userName}\")')
