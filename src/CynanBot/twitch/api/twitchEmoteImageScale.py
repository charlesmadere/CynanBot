from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchEmoteImageScale(Enum):

    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text in ('1.0', 'url_1x'):
            return TwitchEmoteImageScale.SMALL
        elif text in ('2.0', 'url_2x'):
            return TwitchEmoteImageScale.MEDIUM
        elif text in ('3.0', 'url_4x'):
            return TwitchEmoteImageScale.LARGE
        else:
            raise RuntimeError(f'unknown TwitchEmoteImageScale: \"{text}\"')
