from enum import Enum, auto


class PreferredTtsProvider(Enum):

    DEC_TALK = auto()
    GOOGLE = auto()
    MICROSOFT_SAM = auto()
