from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchStreamType(Enum):

    LIVE = auto()
    UNKNOWN = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return TwitchStreamType.UNKNOWN

        text = text.lower()

        if text == 'live':
            return TwitchStreamType.LIVE
        else:
            return TwitchStreamType.UNKNOWN
