from abc import abstractmethod

from .absCheerAction import AbsCheerAction
from .editCheerActionResult.editCheerActionResult import EditCheerActionResult
from ..misc.clearable import Clearable


class CheerActionsRepositoryInterface(Clearable):

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
    async def getActions(self, twitchChannelId: str) -> list[AbsCheerAction]:
        pass

    @abstractmethod
    async def setAction(self, action: AbsCheerAction):
        pass
