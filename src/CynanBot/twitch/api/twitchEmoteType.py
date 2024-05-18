from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchEmoteType(Enum):

    BITS = auto()
    FOLLOWER = auto()
    SUBSCRIPTIONS = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        match text:
            case 'bitstier': return TwitchEmoteType.BITS
            case 'follower': return TwitchEmoteType.FOLLOWER
            case 'subscriptions': return TwitchEmoteType.SUBSCRIPTIONS
            case _: raise ValueError(f'unknown TwitchEmoteType: \"{text}\"')
