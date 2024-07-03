from enum import Enum, auto

from ...misc import utils as utils


class TwitchEmoteImageFormat(Enum):

    ANIMATED = auto()
    DEFAULT = auto()
    STATIC = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            return TwitchEmoteImageFormat.DEFAULT

        text = text.lower()

        match text:
            case 'animated': return TwitchEmoteImageFormat.ANIMATED
            case 'static': return TwitchEmoteImageFormat.STATIC
            case _: return TwitchEmoteImageFormat.DEFAULT
