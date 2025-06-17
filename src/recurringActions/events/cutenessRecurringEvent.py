from typing import Any

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult


class CutenessRecurringEvent(RecurringEvent):

    def __init__(
        self,
        leaderboard: CutenessLeaderboardResult,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not isinstance(leaderboard, CutenessLeaderboardResult):
            raise TypeError(f'leaderboard argument is malformed: \"{leaderboard}\"')

        self.__leaderboard: CutenessLeaderboardResult = leaderboard

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.CUTENESS

    @property
    def leaderboard(self) -> CutenessLeaderboardResult:
        return self.__leaderboard

    def toDictionary(self) -> dict[str, Any]:
        return {
            'eventType': self.eventType,
            'leaderboard': self.__leaderboard,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
