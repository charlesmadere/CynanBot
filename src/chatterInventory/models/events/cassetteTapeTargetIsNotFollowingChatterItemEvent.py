from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..useChatterItemAction import UseChatterItemAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class CassetteTapeTargetIsNotFollowingChatterItemEvent(AbsChatterItemEvent):
    eventId: str
    chatterUserData: TwitchUserInterface
    targetUserData: TwitchUserInterface
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
