from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..absChatterItemAction import AbsChatterItemAction


@dataclass(frozen = True)
class DisabledFeatureChatterItemEvent(AbsChatterItemEvent):
    eventId: str
    originatingAction: AbsChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsChatterItemAction:
        return self.originatingAction
