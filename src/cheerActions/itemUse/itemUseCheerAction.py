from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...chatterInventory.models.chatterItemType import ChatterItemType
from ...misc import utils as utils


class ItemUseCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        itemType: ChatterItemType,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        itemQuantity: int,
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
        elif not utils.isValidInt(itemQuantity):
            raise TypeError(f'itemQuantity argument is malformed: \"{itemQuantity}\"')
        elif itemQuantity < 1 or itemQuantity > utils.getIntMaxSafeSize():
            raise ValueError(f'itemQuantity argument is out of bounds: {itemQuantity}')

        self.__itemType: Final[ChatterItemType] = itemType
        self.__itemQuantity: Final[int] = itemQuantity

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.ITEM_USE

    @property
    def itemQuantity(self) -> int:
        return self.__itemQuantity

    @property
    def itemType(self) -> ChatterItemType:
        return self.__itemType

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, itemType={self.__itemType}, itemQuantity={self.__itemQuantity}'
