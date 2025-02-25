from enum import Enum, auto


class TwitchChatMessageType(Enum):

    CHANNEL_POINTS_HIGHLIGHTED = auto()
    CHANNEL_POINTS_SUB_ONLY = auto()
    POWER_UPS_GIGANTIFIED_EMOTE = auto()
    POWER_UPS_MESSAGE_EFFECT = auto()
    USER_INTRO = auto()
