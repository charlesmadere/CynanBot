from enum import Enum, auto


class AddVoicemailResult(Enum):

    FEATURE_DISABLED = auto()
    MAXIMUM_FOR_TARGET_USER = auto()
    MESSAGE_MALFORMED = auto()
    OK = auto()
    TARGET_USER_IS_ORIGINATING_USER = auto()
    TARGET_USER_IS_TWITCH_CHANNEL_USER = auto()
