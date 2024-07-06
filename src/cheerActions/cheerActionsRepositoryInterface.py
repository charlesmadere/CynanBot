from abc import abstractmethod

from .absCheerAction import AbsCheerAction
from .cheerAction import CheerAction
from .cheerActionBitRequirement import CheerActionBitRequirement
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc.clearable import Clearable


class CheerActionsRepositoryInterface(Clearable):

    @abstractmethod
    async def addAction(
        self,
        bitRequirement: CheerActionBitRequirement,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        bits: int,
        durationSeconds: int | None,
        tag: str | None,
        twitchChannelId: str
    ) -> CheerAction:
        pass

    @abstractmethod
    async def deleteAction(self, bits: int, userId: str) -> CheerAction | None:
        pass

    @abstractmethod
    async def getAction(self, bits: int, userId: str) -> CheerAction | None:
        pass

    @abstractmethod
    async def getActions(self, userId: str) -> list[CheerAction]:
        pass

    @abstractmethod
    async def setAction(self, action: AbsCheerAction):
        pass
