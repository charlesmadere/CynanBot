from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..itemDetails.animalPetItemDetails import AnimalPetItemDetails
from ..useChatterItemAction import UseChatterItemAction
from ....emojiHelper.emojiData import EmojiData


@dataclass(frozen = True, slots = True)
class AnimalPetChatterItemEvent(AbsChatterItemEvent):
    itemDetails: AnimalPetItemDetails
    updatedInventory: ChatterInventoryData | None
    animalEmoji: EmojiData
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
