from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchRewardRedemptionStatus(Enum):

    CANCELED = auto()
    FULFILLED = auto()
    UNFULFILLED = auto()
    UNKNOWN = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        match text:
            case 'canceled': return TwitchRewardRedemptionStatus.CANCELED
            case 'fulfilled': return TwitchRewardRedemptionStatus.FULFILLED
            case 'unfulfilled': return TwitchRewardRedemptionStatus.UNFULFILLED
            case 'unknown': return TwitchRewardRedemptionStatus.UNKNOWN
            case _: return None
