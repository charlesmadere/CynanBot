from enum import Enum, auto


class TtsMonsterDonationPrefixConfig(Enum):

    DISABLED = auto()
    ENABLED = auto()
    IF_MESSAGE_IS_BLANK = auto()
