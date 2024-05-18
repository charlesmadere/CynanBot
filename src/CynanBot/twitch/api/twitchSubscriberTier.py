from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchSubscriberTier(Enum):

    PRIME = auto()
    TIER_ONE = auto()
    TIER_TWO = auto()
    TIER_THREE = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        match text:
            case 'prime': return TwitchSubscriberTier.PRIME
            case '1000': return TwitchSubscriberTier.TIER_ONE
            case '2000': return TwitchSubscriberTier.TIER_TWO
            case '3000': return TwitchSubscriberTier.TIER_THREE
            case _: raise ValueError(f'unknown TwitchSubscriberTier: \"{text}\"')
