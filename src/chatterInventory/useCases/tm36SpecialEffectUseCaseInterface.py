from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.chatterInventoryData import ChatterInventoryData
from ..models.useChatterItemAction import UseChatterItemAction


class Tm36SpecialEffectUseCaseInterface(ABC):

    class AbsSpecialEffect(ABC):
        pass

    @dataclass(frozen = True, slots = True)
    class DudSpecialEffect(AbsSpecialEffect):
        updatedInventory: ChatterInventoryData | None
        gottemEmote: str

    @dataclass(frozen = True, slots = True)
    class NoSpecialEffect(AbsSpecialEffect):
        pass

    @abstractmethod
    async def invoke(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> AbsSpecialEffect:
        pass
