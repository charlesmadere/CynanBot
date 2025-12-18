from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...chatterInventory.models.chatterItemType import ChatterItemType


class ItemUseCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        itemType: ChatterItemType,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        twitchChannelId: str,
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')

        self.__itemType: Final[ChatterItemType] = itemType

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.ITEM_USE

    @property
    def itemType(self) -> ChatterItemType:
        return self.__itemType

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, itemType={self.__itemType}'
