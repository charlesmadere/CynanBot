from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchEmoteType(Enum):

    BITS = auto()
    FOLLOWER = auto()
    SUBSCRIPTIONS = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'bitstier':
            return TwitchEmoteType.BITS
        elif text == 'follower':
            return TwitchEmoteType.FOLLOWER
        elif text == 'subscriptions':
            return TwitchEmoteType.SUBSCRIPTIONS
        else:
            raise RuntimeError(f'unknown TwitchEmoteType: \"{text}\"')
