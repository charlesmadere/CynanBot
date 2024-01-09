from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchWebsocketRewardRedemptionStatus(Enum):

    CANCELED = auto()
    FULFILLED = auto()
    UNFULFILLED = auto()
    UNKNOWN = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'canceled':
            return TwitchWebsocketRewardRedemptionStatus.CANCELED
        elif text == 'fulfilled':
            return TwitchWebsocketRewardRedemptionStatus.FULFILLED
        elif text == 'unfulfilled':
            return TwitchWebsocketRewardRedemptionStatus.UNFULFILLED
        elif text == 'unknown':
            return TwitchWebsocketRewardRedemptionStatus.UNKNOWN
        else:
            return None
