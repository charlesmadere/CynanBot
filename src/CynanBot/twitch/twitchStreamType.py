from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchStreamType(Enum):

    LIVE = auto()
    UNKNOWN = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return TwitchStreamType.UNKNOWN

        text = text.lower()

        if text == 'live':
            return TwitchStreamType.LIVE
        else:
            return TwitchStreamType.UNKNOWN
