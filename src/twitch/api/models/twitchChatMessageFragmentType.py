from enum import Enum, auto


class TwitchChatMessageFragmentType(Enum):

    CHEERMOTE = auto()
    EMOTE = auto()
    MENTION = auto()
    TEXT = auto()
