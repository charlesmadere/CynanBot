from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult


@dataclass(frozen = True)
class CutenessRecurringEvent(RecurringEvent):
    leaderboard: CutenessLeaderboardResult
    twitchChannel: str
    twitchChannelId: str

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.CUTENESS
