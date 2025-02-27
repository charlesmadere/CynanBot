from abc import ABC, abstractmethod

from frozendict import frozendict

from .absCheerAction import AbsCheerAction
from .editCheerActionResult.editCheerActionResult import EditCheerActionResult
from ..misc.clearable import Clearable


class CheerActionsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def deleteAction(self, bits: int, twitchChannelId: str) -> AbsCheerAction | None:
        pass

    @abstractmethod
    async def disableAction(self, bits: int, twitchChannelId: str) -> EditCheerActionResult:
        pass

    @abstractmethod
    async def enableAction(self, bits: int, twitchChannelId: str) -> EditCheerActionResult:
        pass

    @abstractmethod
    async def getAction(self, bits: int, twitchChannelId: str) -> AbsCheerAction | None:
        pass

    @abstractmethod
    async def getActions(self, twitchChannelId: str) -> frozendict[int, AbsCheerAction]:
        pass

    @abstractmethod
    async def setAction(self, action: AbsCheerAction):
        pass
