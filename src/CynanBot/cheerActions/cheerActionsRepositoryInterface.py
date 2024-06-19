from abc import abstractmethod

from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.misc.clearable import Clearable


class CheerActionsRepositoryInterface(Clearable):

    @abstractmethod
    async def addAction(
        self,
        bitRequirement: CheerActionBitRequirement,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: int,
        tag: str | None,
        userId: str
    ) -> CheerAction:
        pass

    @abstractmethod
    async def deleteAction(self, actionId: str, userId: str) -> CheerAction | None:
        pass

    @abstractmethod
    async def getAction(self, actionId: str, userId: str) -> CheerAction | None:
        pass

    @abstractmethod
    async def getActions(self, userId: str) -> list[CheerAction]:
        pass
