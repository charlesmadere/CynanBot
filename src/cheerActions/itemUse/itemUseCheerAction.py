from dataclasses import dataclass

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...chatterInventory.models.chatterItemType import ChatterItemType


@dataclass(frozen = True, slots = True)
class ItemUseCheerAction(AbsCheerAction):
    enabled: bool
    itemType: ChatterItemType
    streamStatusRequirement: CheerActionStreamStatusRequirement
    bits: int
    twitchChannelId: str

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.ITEM_USE

    def getBits(self) -> int:
        return self.bits

    def getStreamStatusRequirement(self) -> CheerActionStreamStatusRequirement:
        return self.streamStatusRequirement

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def isEnabled(self) -> bool:
        return self.enabled

    def printOut(self) -> str:
        return f'isEnabled={self.enabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, itemType={self.itemType}'
