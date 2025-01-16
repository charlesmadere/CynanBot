from abc import ABC, abstractmethod

from .addOrRemoveUserData import AddOrRemoveUserData


class AddOrRemoveUserEventListener(ABC):

    @abstractmethod
    async def onAddOrRemoveUserEvent(self, event: AddOrRemoveUserData):
        pass
