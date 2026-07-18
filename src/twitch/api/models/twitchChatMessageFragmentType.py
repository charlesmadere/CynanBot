from enum import Enum, auto


class TwitchChatMessageFragmentType(Enum):

    CHEERMOTE = auto()
    EMOTE = auto()
    GIF = auto()
    MENTION = auto()
    TEXT = auto()
