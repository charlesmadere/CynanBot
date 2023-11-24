from abc import ABC, abstractmethod

from users.modifyUserData import ModifyUserData


class ModifyUserEventListener(ABC):

    @abstractmethod
    async def onModifyUserEvent(self, event: ModifyUserData):
        pass
