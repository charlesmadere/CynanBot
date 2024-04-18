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

        if text == 'canceled':
            return TwitchRewardRedemptionStatus.CANCELED
        elif text == 'fulfilled':
            return TwitchRewardRedemptionStatus.FULFILLED
        elif text == 'unfulfilled':
            return TwitchRewardRedemptionStatus.UNFULFILLED
        elif text == 'unknown':
            return TwitchRewardRedemptionStatus.UNKNOWN
        else:
            return None
