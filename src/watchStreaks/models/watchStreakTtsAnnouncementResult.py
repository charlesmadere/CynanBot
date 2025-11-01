from enum import Enum, auto


class WatchStreakTtsAnnouncementResult(Enum):

    NOT_ENABLED = auto()
    OK = auto()
    STREAK_TOO_SHORT = auto()
