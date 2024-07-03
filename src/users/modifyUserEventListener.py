from abc import ABC, abstractmethod

from .modifyUserData import ModifyUserData


class ModifyUserEventListener(ABC):

    @abstractmethod
    async def onModifyUserEvent(self, event: ModifyUserData):
        pass
