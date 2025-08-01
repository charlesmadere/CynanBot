from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..grenadeTimeoutAction import GrenadeTimeoutAction
from ..grenadeTimeoutTarget import GrenadeTimeoutTarget
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult


@dataclass(frozen = True)
class GrenadeTimeoutEvent(AbsTimeoutEvent):
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    originatingAction: GrenadeTimeoutAction
    target: GrenadeTimeoutTarget
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
