from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..absChatterItemAction import AbsChatterItemAction


@dataclass(frozen = True)
class DisabledFeatureChatterItemEvent(AbsChatterItemEvent):
    originatingAction: AbsChatterItemAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsChatterItemAction:
        return self.originatingAction
