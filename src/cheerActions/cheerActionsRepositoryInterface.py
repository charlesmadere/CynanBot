from abc import abstractmethod

from .cheerAction import CheerAction
from .cheerActionBitRequirement import CheerActionBitRequirement
from .cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc.clearable import Clearable


class CheerActionsRepositoryInterface(Clearable):

    @abstractmethod
    async def addAction(
        self,
        bitRequirement: CheerActionBitRequirement,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: int | None,
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
