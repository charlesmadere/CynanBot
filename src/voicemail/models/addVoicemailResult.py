from enum import Enum, auto


class AddVoicemailResult(Enum):

    MAXIMUM_FOR_TARGET_USER = auto()
    MESSAGE_MALFORMED = auto()
    OK = auto()
