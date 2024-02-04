from enum import Enum, auto


class StreamAlertState(Enum):

    NOT_STARTED = auto()
    SOUND = auto()
    TTS = auto()
