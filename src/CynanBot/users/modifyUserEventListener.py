from abc import ABC, abstractmethod

from CynanBot.users.modifyUserData import ModifyUserData


class ModifyUserEventListener(ABC):

    @abstractmethod
    async def onModifyUserEvent(self, event: ModifyUserData):
        pass
