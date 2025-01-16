from enum import Enum, auto


class StreamAlertState(Enum):

    NOT_STARTED = auto()
    SOUND_FINISHED = auto()
    SOUND_STARTED = auto()
    TTS_FINISHED = auto()
    TTS_STARTED = auto()
