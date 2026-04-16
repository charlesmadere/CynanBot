from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchWatchStreak:
    channelPointsAwarded: int
    streakCount: int
