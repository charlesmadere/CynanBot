from typing import Any, Final

from .itemUseStep import ItemUseStep
from .itemUseSteps import ItemUseSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....chatterInventory.models.chatterItemType import ChatterItemType
from ....misc import utils as utils


class ItemUseWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__steps: Final[ItemUseSteps] = ItemUseSteps()
        self.__itemType: ChatterItemType | None = None
        self.__bits: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.ITEM_USE

    @property
    def currentStep(self) -> ItemUseStep:
        return self.__steps.currentStep

    @property
    def itemType(self) -> ChatterItemType | None:
        return self.__itemType

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__itemType=}'

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def requireItemType(self) -> ChatterItemType:
        itemType = self.__itemType

        if itemType is None:
            raise ValueError(f'itemType value has not been set: ({self=})')

        return itemType

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    def setItemType(self, itemType: ChatterItemType):
        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')

        self.__itemType = itemType

    @property
    def steps(self) -> ItemUseSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'currentStep': self.currentStep,
            'itemType': self.__itemType,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
