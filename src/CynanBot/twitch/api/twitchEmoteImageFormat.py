from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchEmoteImageFormat(Enum):

    ANIMATED = auto()
    DEFAULT = auto()
    STATIC = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            return TwitchEmoteImageFormat.DEFAULT

        text = text.lower()

        if text == 'animated':
            return TwitchEmoteImageFormat.ANIMATED
        elif text == 'static':
            return TwitchEmoteImageFormat.STATIC
        else:
            return TwitchEmoteImageFormat.DEFAULT
