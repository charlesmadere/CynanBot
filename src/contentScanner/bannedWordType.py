from enum import Enum, auto


class BannedWordType(Enum):

    EXACT_WORD = auto()
    PHRASE = auto()
