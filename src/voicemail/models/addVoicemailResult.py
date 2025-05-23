from enum import Enum, auto


class AddVoicemailResult(Enum):

    MAXIMUM_ALREADY_SET = auto()
    OK = auto()
    TARGET_USER_ALREADY_SET = auto()
