from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchSubscriberTier(Enum):

    PRIME = auto()
    TIER_ONE = auto()
    TIER_TWO = auto()
    TIER_THREE = auto()

    @classmethod
    def fromStr(ctls, text: Optional[str]):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'prime':
            return TwitchSubscriberTier.PRIME
        elif text == '1000':
            return TwitchSubscriberTier.TIER_ONE
        elif text == '2000':
            return TwitchSubscriberTier.TIER_TWO
        elif text == '3000':
            return TwitchSubscriberTier.TIER_THREE
        else:
            raise ValueError(f'unknown TwitchSubscriberTier: \"{text}\"')
