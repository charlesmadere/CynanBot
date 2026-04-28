from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class CutenessRecurringEvent(RecurringEvent):
    leaderboard: CutenessLeaderboardResult
    twitchChannelId: str
    twitchUser: UserInterface

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.CUTENESS

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchUser(self) -> UserInterface:
        return self.twitchUser
