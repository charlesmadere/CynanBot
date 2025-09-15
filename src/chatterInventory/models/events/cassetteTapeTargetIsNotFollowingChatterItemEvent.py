from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class CassetteTapeTargetIsNotFollowingChatterItemEvent(AbsChatterItemEvent):
    chatterUserName: str
    eventId: str
    targetUserId: str
    targetUserName: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
