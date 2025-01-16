from abc import abstractmethod

from .addOrRemoveUserActionType import AddOrRemoveUserActionType
from .addOrRemoveUserData import AddOrRemoveUserData
from .addOrRemoveUserEventListener import AddOrRemoveUserEventListener
from ..misc.clearable import Clearable


class AddOrRemoveUserDataHelperInterface(Clearable):

    @abstractmethod
    async def clearCaches(self):
        pass

    @abstractmethod
    async def getData(self) -> AddOrRemoveUserData | None:
        pass

    @abstractmethod
    async def notifyAddOrRemoveUserEventListenerAndClearData(self):
        pass

    @abstractmethod
    def setAddOrRemoveUserEventListener(self, listener: AddOrRemoveUserEventListener | None):
        pass

    @abstractmethod
    async def setUserData(
        self,
        actionType: AddOrRemoveUserActionType,
        userId: str,
        userName: str
    ):
        pass
