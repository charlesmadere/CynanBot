from abc import abstractmethod
from typing import List, Optional

from cheerActions.cheerAction import CheerAction
from cheerActions.cheerActionRequirement import CheerActionRequirement
from cheerActions.cheerActionType import CheerActionType
from misc.clearable import Clearable


class CheerActionsRepositoryInterface(Clearable):

    @abstractmethod
    async def addAction(
        self,
        actionRequirement: CheerActionRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: Optional[int],
        userId: str
    ) -> CheerAction:
        pass

    @abstractmethod
    async def deleteAction(self, actionId: str, userId: str) -> Optional[CheerAction]:
        pass

    @abstractmethod
    async def getAction(self, actionId: str, userId: str) -> Optional[CheerAction]:
        pass

    @abstractmethod
    async def getActions(self, userId: str) -> List[CheerAction]:
        pass
