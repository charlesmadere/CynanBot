from enum import Enum, auto


class WatchStreakTtsAnnouncementResult(Enum):

    NOT_ENABLED = auto()
    SUBMITTED_TTS_EVENT = auto()
    STREAK_TOO_SHORT = auto()
